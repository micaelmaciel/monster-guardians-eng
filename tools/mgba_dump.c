/* Headless mGBA harvester: run a GBA ROM, feed scheduled input, dump memory.
 *
 * Build: gcc -O2 -o mgba_dump mgba_dump.c -lmgba
 * Usage: mgba_dump <rom> <outdir> [frames_csv] [input_spec]
 *   frames_csv:  frame numbers to dump, e.g. "60,300,600"
 *   input_spec:  "start-end:KEY+KEY,..." e.g. "240-250:START,300-320:A"
 * Keys: A B SELECT START RIGHT LEFT UP DOWN R L
 */
#include <mgba/core/core.h>
#include <mgba/core/config.h>
#include <mgba/core/input.h>
#include <mgba/core/serialize.h>
#include <mgba/internal/gba/input.h>
#include <mgba/internal/gba/gba.h>
#include <mgba-util/vfs.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>

/* Executive PC must be inside a mapped bus region; anything else means the
 * program jumped into garbage (usually a smashed return address). */
static int mgba_pc_valid(uint32_t pc) {
    if (pc < 0x00004000) return 1;                        /* BIOS */
    if (pc >= 0x02000000 && pc < 0x02040000) return 1;    /* EWRAM */
    if (pc >= 0x03000000 && pc < 0x03008000) return 1;    /* IWRAM */
    if (pc >= 0x04000000 && pc < 0x04000400) return 1;    /* IO */
    if (pc >= 0x05000000 && pc < 0x05000400) return 1;    /* palette */
    if (pc >= 0x06000000 && pc < 0x06018000) return 1;    /* VRAM */
    if (pc >= 0x07000000 && pc < 0x07000400) return 1;    /* OAM */
    if (pc >= 0x08000000 && pc < 0x08800000) return 1;    /* ROM (8 MiB cart) */
    if (pc >= 0x0E000000 && pc < 0x0E010000) return 1;    /* SRAM */
    return 0;
}

static uint32_t keybit(const char* name) {
    if (!strcmp(name, "A")) return 1 << GBA_KEY_A;
    if (!strcmp(name, "B")) return 1 << GBA_KEY_B;
    if (!strcmp(name, "SELECT")) return 1 << GBA_KEY_SELECT;
    if (!strcmp(name, "START")) return 1 << GBA_KEY_START;
    if (!strcmp(name, "RIGHT")) return 1 << GBA_KEY_RIGHT;
    if (!strcmp(name, "LEFT")) return 1 << GBA_KEY_LEFT;
    if (!strcmp(name, "UP")) return 1 << GBA_KEY_UP;
    if (!strcmp(name, "DOWN")) return 1 << GBA_KEY_DOWN;
    if (!strcmp(name, "R")) return 1 << GBA_KEY_R;
    if (!strcmp(name, "L")) return 1 << GBA_KEY_L;
    return 0;
}

static void dump_region(struct mCore* core, uint32_t base, uint32_t size, const char* dir, const char* name) {
    char path[512];
    snprintf(path, sizeof(path), "%s/%s.bin", dir, name);
    FILE* f = fopen(path, "wb");
    if (!f) { perror(path); return; }
    unsigned char buf[4096];
    for (uint32_t off = 0; off < size; off += sizeof(buf)) {
        uint32_t n = size - off < sizeof(buf) ? size - off : sizeof(buf);
        for (uint32_t i = 0; i < n; i++) buf[i] = core->busRead8(core, base + off + i);
        fwrite(buf, 1, n, f);
    }
    fclose(f);
}

static void write_ppm(color_t* pixels, const char* dir, const char* name) {
    if (!pixels) return;
    size_t stride = 240 * sizeof(color_t);
    char path[512];
    snprintf(path, sizeof(path), "%s/%s.ppm", dir, name);
    FILE* f = fopen(path, "wb");
    if (!f) return;
    fprintf(f, "P6\n240 160\n255\n");
    for (int y = 0; y < 160; y++) {
        const color_t* row = (const color_t*)((const char*)pixels + y * stride);
        for (int x = 0; x < 240; x++) {
            color_t c = row[x];
            unsigned char rgb[3] = {
                (unsigned char)(c & 0xFF),          /* R */
                (unsigned char)((c >> 8) & 0xFF),   /* G */
                (unsigned char)((c >> 16) & 0xFF) } /* B */;
            fwrite(rgb, 1, 3, f);
        }
    }
    fclose(f);
}

int main(int argc, char** argv) {
    if (argc < 3) { fprintf(stderr, "usage: %s <rom> <outdir> [frames_csv] [input_spec]\n", argv[0]); return 1; }
    const char* rom = argv[1];
    const char* outdir = argv[2];
    const char* frames_csv = argc > 3 ? argv[3] : "120,300,480,600,720,900";
    const char* input_spec = argc > 4 ? argv[4] : "240-260:START,320-340:A,420-440:START,500-540:A";

    mkdir(outdir, 0777);

    struct mCore* core = mCoreFind(rom);
    if (!core) { fprintf(stderr, "cannot create core for %s\n", rom); return 1; }
    core->init(core);
    mCoreInitConfig(core, "mgba");
    mCoreConfigSetDefaultValue(&core->config, "idleOptimization", "remove");
    mCoreConfigSetDefaultIntValue(&core->config, "logToStdout", 0);
    mCoreConfigSetDefaultIntValue(&core->config, "logLevel", 0);
    mInputMapInit(&core->inputMap, &GBAInputInfo);
    if (!mCoreLoadFile(core, rom)) { fprintf(stderr, "loadROM failed\n"); return 1; }
    const char* sav = getenv("MGBA_SAV");
    if (sav && *sav) {
        if (mCoreLoadSaveFile(core, sav, false)) fprintf(stderr, "loaded save %s\n", sav);
        else fprintf(stderr, "save load failed: %s\n", sav);
    }
    core->reset(core);

    color_t* vbuf = calloc(240 * 160, sizeof(color_t));
    core->setVideoBuffer(core, vbuf, 240);
    /* Associate the software renderer now that an output buffer exists. */
    core->reloadConfigOption(core, "hwaccelVideo", &core->config);

    const char* statein = getenv("MGBA_STATE_IN");
    if (statein && *statein) {
        struct VFile* vf = VFileOpen(statein, O_RDONLY);
        if (vf) {
            bool ok = mCoreLoadStateNamed(core, vf, SAVESTATE_ALL);
            vf->close(vf);
            fprintf(stderr, "state %s %s\n", ok ? "loaded" : "LOAD FAILED", statein);
        } else {
            fprintf(stderr, "cannot open state %s\n", statein);
        }
    }

    /* parse dump frames */
    int frames[1024]; int nframes = 0;
    { char* tmp = strdup(frames_csv); char* tok = strtok(tmp, ",");
      while (tok && nframes < 1024) { frames[nframes++] = atoi(tok); tok = strtok(NULL, ","); } free(tmp); }
    int maxframe = 0;
    for (int i = 0; i < nframes; i++) if (frames[i] > maxframe) maxframe = frames[i];

    /* parse input windows (strtok_r: inner/outer tokenizers must not share state) */
    struct { int a, b; uint32_t keys; } inputs[8192]; int nin = 0;
    { char* tmp = strdup(input_spec); char* s1 = NULL; char* s2 = NULL; char* tok = strtok_r(tmp, ",", &s1);
      while (tok && nin < 8192) {
        char* colon = strchr(tok, ':');
        if (colon) { *colon = 0;
            int a = 0, b = 0;
            if (sscanf(tok, "%d-%d", &a, &b) < 2) { a = b = atoi(tok); }
            uint32_t keys = 0; char* k = strtok_r(colon + 1, "+", &s2);
            while (k) { keys |= keybit(k); k = strtok_r(NULL, "+", &s2); }
            inputs[nin].a = a; inputs[nin].b = b; inputs[nin].keys = keys; nin++;
        }
        tok = strtok_r(NULL, ",", &s1); } free(tmp); }
    fprintf(stderr, "input windows parsed: %d\n", nin);

    /* parse poke list: addr=value[:size],... (simulates cheat codes) */
    struct { uint32_t addr, value; int size; } pokes[64]; int npokes = 0;
    const char* pokeenv = getenv("MGBA_POKE");
    if (pokeenv && *pokeenv) {
        char* tmp = strdup(pokeenv); char* s1 = NULL;
        char* tok = strtok_r(tmp, ",", &s1);
        while (tok && npokes < 64) {
            char* eq = strchr(tok, '=');
            if (eq) {
                *eq = 0;
                char* vs = eq + 1;
                int size = 2;
                char* colon = strchr(vs, ':');
                if (colon) { *colon = 0; size = atoi(colon + 1); }
                pokes[npokes].addr = (uint32_t)strtoul(tok, NULL, 0);
                pokes[npokes].value = (uint32_t)strtoul(vs, NULL, 0);
                pokes[npokes].size = size;
                npokes++;
            }
            tok = strtok_r(NULL, ",", &s1);
        }
        free(tmp);
        fprintf(stderr, "pokes parsed: %d\n", npokes);
    }
    const char* pokeframe_env = getenv("MGBA_POKE_FRAME");
    int poke_frame = (pokeframe_env && *pokeframe_env) ? atoi(pokeframe_env) : 0;
    const char* pokeevery_env = getenv("MGBA_POKE_EVERY");
    int poke_every = pokeevery_env && *pokeevery_env;

    struct GBA* gba = core->board;
    uint32_t pchist[256]; int pchist_n = 0, pchist_pos = 0;

    const char* traceenv = getenv("MGBA_TRACE_FROM");
    int trace_from = (traceenv && *traceenv) ? atoi(traceenv) : -1;

    for (int frame = 0; frame <= maxframe; frame++) {
        uint32_t keys = 0;
        for (int i = 0; i < nin; i++)
            if (frame >= inputs[i].a && frame <= inputs[i].b) keys |= inputs[i].keys;
        core->setKeys(core, keys);
        if (npokes && (frame == poke_frame || (poke_every && frame >= poke_frame))) {
            for (int i = 0; i < npokes; i++) {
                switch (pokes[i].size) {
                case 1: core->busWrite8(core, pokes[i].addr, pokes[i].value); break;
                case 4: core->busWrite32(core, pokes[i].addr, pokes[i].value); break;
                default: core->busWrite16(core, pokes[i].addr, pokes[i].value); break;
                }
            }
        }
        core->runFrame(core);
        const char* stateout = getenv("MGBA_STATE_OUT");
        if (stateout && *stateout) {
            const char* sfenval = getenv("MGBA_STATE_FRAME");
            int sf = (sfenval && *sfenval) ? atoi(sfenval) : 0;
            if (frame == sf) {
                struct VFile* vf = VFileOpen(stateout, O_WRONLY | O_CREAT | O_TRUNC);
                if (vf) {
                    mCoreSaveStateNamed(core, vf, SAVESTATE_ALL);
                    vf->close(vf);
                    fprintf(stderr, "state saved frame %d -> %s\n", frame, stateout);
                }
            }
        }
        const char* pcsample_env = getenv("MGBA_PCSAMPLE");
        if (pcsample_env && *pcsample_env && frame == atoi(pcsample_env) && core->step && gba && gba->cpu) {
            enum { PCS_MAX = 4096 };
            static uint32_t pcs[PCS_MAX], cnts[PCS_MAX];
            int npcs = 0;
            long samples = 0;
            const char* nenv = getenv("MGBA_PCSAMPLE_STEPS");
            long want = (nenv && *nenv) ? atol(nenv) : 2000000L;
            for (; samples < want; samples++) {
                uint32_t pc = gba->cpu->gprs[15] & ~1u;
                int found = -1;
                for (int i = 0; i < npcs; i++) if (pcs[i] == pc) { found = i; break; }
                if (found >= 0) cnts[found]++;
                else if (npcs < PCS_MAX) { pcs[npcs] = pc; cnts[npcs] = 1; npcs++; }
                core->step(core);
            }
            printf("PCSAMPLE frame=%d steps=%ld unique=%d\n", frame, samples, npcs);
            for (int rank = 0; rank < 90; rank++) {
                int best = -1;
                for (int i = 0; i < npcs; i++) {
                    if (cnts[i] && (best < 0 || cnts[i] > cnts[best])) best = i;
                }
                if (best < 0) break;
                printf("  pc=%08X n=%u (%.1f%%)\n", pcs[best], cnts[best], 100.0 * cnts[best] / samples);
                cnts[best] = 0;
            }
            fflush(stdout);
        }
        const char* watch_env = getenv("MGBA_WATCH_BYTE");
        const char* watch_from_env = getenv("MGBA_WATCH_FROM");
        int watch_from = (watch_from_env && *watch_from_env) ? atoi(watch_from_env) : 0;
        if (watch_env && *watch_env && core->step && gba && gba->cpu && frame >= watch_from) {
            uint32_t addr = (uint32_t)strtoul(watch_env, NULL, 16);
            uint8_t* base = NULL;
            uint32_t off = 0;
            if (addr >= 0x03000000 && addr < 0x03008000) { base = (uint8_t*)gba->memory.iwram; off = addr - 0x03000000; }
            else if (addr >= 0x02000000 && addr < 0x02040000) { base = (uint8_t*)gba->memory.wram; off = addr - 0x02000000; }
            else if (addr >= 0x06000000 && addr < 0x06018000) { base = (uint8_t*)gba->video.vram; off = addr - 0x06000000; }
            if (base) {
                const char* stop_env = getenv("MGBA_WATCH_STOP");
                int stop_val = (stop_env && *stop_env) ? (int)strtol(stop_env, NULL, 0) : -1;
                const char* maxenv = getenv("MGBA_WATCH_MAX");
                int max_changes = (maxenv && *maxenv) ? atoi(maxenv) : 1;
                const char* stepsenv = getenv("MGBA_WATCH_STEPS");
                long budget = (stepsenv && *stepsenv) ? atol(stepsenv) : 300000000L;
                static uint32_t hist[256][10];
                int hn = 0, hp = 0;
                uint8_t prev = base[off];
                long steps = 0;
                int changes = 0;
                uint32_t lastfc = core->frameCounter ? core->frameCounter(core) : (uint32_t)frame;
                for (; steps < budget; steps++) {
                    if ((steps & 0xFFF) == 0 && core->frameCounter) {
                        uint32_t fc = core->frameCounter(core);
                        if (fc != lastfc) {
                            lastfc = fc;
                            uint32_t wk = 0;
                            for (int i = 0; i < nin; i++)
                                if ((int)fc >= inputs[i].a && (int)fc <= inputs[i].b) wk |= inputs[i].keys;
                            core->setKeys(core, wk);
                        }
                    }
                    uint32_t pc = gba->cpu->gprs[15] & ~1u;
                    hist[hp][0] = pc;
                    hist[hp][1] = gba->cpu->gprs[0];
                    hist[hp][2] = gba->cpu->gprs[1];
                    hist[hp][3] = gba->cpu->gprs[2];
                    hist[hp][4] = gba->cpu->gprs[3];
                    hist[hp][5] = gba->cpu->gprs[4];
                    hist[hp][6] = gba->cpu->gprs[5];
                    hist[hp][7] = gba->cpu->gprs[6];
                    hist[hp][8] = gba->cpu->gprs[13];
                    hist[hp][9] = gba->cpu->gprs[14];
                    hp = (hp + 1) & 255; if (hn < 256) hn++;
                    core->step(core);
                    uint8_t now = base[off];
                    if (now != prev) {
                        uint32_t fnow = core->frameCounter ? core->frameCounter(core) : (uint32_t)frame;
                        printf("WATCH frame=%u addr=%08X %02X->%02X pc=%08X lr=%08X sp=%08X steps=%ld\n",
                               fnow, addr, prev, now, pc, gba->cpu->gprs[14], gba->cpu->gprs[13], steps);
                        int n = hn < 28 ? hn : 28;
                        for (int i = n - 1; i >= 0; i--) {
                            int idx = (hp - 1 - i) & 255;
                            uint32_t* e = hist[idx];
                            printf("  H %08X r0=%08X r1=%08X r2=%08X r3=%08X r4=%08X r5=%08X r6=%08X sp=%08X lr=%08X\n",
                                   e[0], e[1], e[2], e[3], e[4], e[5], e[6], e[7], e[8], e[9]);
                        }
                        uint32_t spv = gba->cpu->gprs[13] & ~3u;
                        if (spv >= 0x03000000 && spv < 0x03008000) {
                            uint32_t* st = (uint32_t*)((uint8_t*)gba->memory.iwram + (spv - 0x03000000));
                            for (int i = 0; i < 160; i++) printf("  STK %08X: %08X\n", spv + i * 4, st[i]);
                        }
                        fflush(stdout);
                        changes++;
                        prev = now;
                        if ((stop_val >= 0 && (int)now == stop_val) || changes >= max_changes) return 0;
                    }
                }
                printf("WATCH done changes=%d after %ld steps frame=%d\n", changes, steps, frame);
                fflush(stdout);
                return 0;
            }
        }
        if (frame == trace_from && core->step && gba && gba->cpu) {
            static uint32_t ring[128][10]; int rn = 0, rp = 0;
            long steps;
            for (steps = 0; steps < 200000000L; steps++) {
                uint32_t pc = gba->cpu->gprs[15] & ~1u;
                if (!mgba_pc_valid(pc)) {
                    printf("TRACE CRASH step=%ld pc=%08X lr=%08X sp=%08X\n", steps, pc,
                           gba->cpu->gprs[14], gba->cpu->gprs[13]);
                    for (int i = 0; i < rn; i++) {
                        int idx = (rp - rn + i) & 127;
                        uint32_t* e = ring[idx];
                        printf("  %08X r0=%08X r1=%08X r2=%08X r3=%08X r4=%08X sp=%08X lr=%08X\n",
                               e[0], e[1], e[2], e[3], e[4], e[5], e[6], e[7]);
                    }
                    fflush(stdout);
                    break;
                }
                ring[rp][0] = pc;
                ring[rp][1] = gba->cpu->gprs[0];
                ring[rp][2] = gba->cpu->gprs[1];
                ring[rp][3] = gba->cpu->gprs[2];
                ring[rp][4] = gba->cpu->gprs[3];
                ring[rp][5] = gba->cpu->gprs[4];
                ring[rp][6] = gba->cpu->gprs[13];
                ring[rp][7] = gba->cpu->gprs[14];
                rp = (rp + 1) & 127; if (rn < 128) rn++;
                core->step(core);
            }
            if (steps >= 200000000L) printf("TRACE no crash after %ld steps\n", steps);
            break;
        }
        if (gba && gba->cpu) {
            uint32_t pc = gba->cpu->gprs[15] & ~1u;
            pchist[pchist_pos] = pc; pchist_pos = (pchist_pos + 1) & 255; if (pchist_n < 256) pchist_n++;
            if (!mgba_pc_valid(pc)) {
                printf("CRASH frame=%d pc=%08X lr=%08X sp=%08X\n", frame, pc,
                       gba->cpu->gprs[14], gba->cpu->gprs[13]);
                char name[512];
                snprintf(name, sizeof(name), "%s/crash_pcs.txt", outdir);
                FILE* pf = fopen(name, "w");
                if (pf) {
                    for (int i = 0; i < pchist_n; i++) {
                        int idx = (pchist_pos - pchist_n + i) & 255;
                        fprintf(pf, "%d %08X\n", frame - pchist_n + 1 + i, pchist[idx]);
                    }
                    fclose(pf);
                }
                snprintf(name, sizeof(name), "crash_vram"); dump_region(core, 0x06000000, 0x18000, outdir, name);
                snprintf(name, sizeof(name), "crash_ewram"); dump_region(core, 0x02000000, 0x40000, outdir, name);
                snprintf(name, sizeof(name), "crash_iwram"); dump_region(core, 0x03000000, 0x8000, outdir, name);
                snprintf(name, sizeof(name), "crash_pal"); dump_region(core, 0x05000000, 0x400, outdir, name);
                snprintf(name, sizeof(name), "crash_oam"); dump_region(core, 0x07000000, 0x400, outdir, name);
                snprintf(name, sizeof(name), "crash_io"); dump_region(core, 0x04000000, 0x400, outdir, name);
                snprintf(name, sizeof(name), "crash_shot"); write_ppm(vbuf, outdir, name);
                break;
            }
        }
        bool need_dump = false;
        for (int i = 0; i < nframes; i++) if (frames[i] == frame) need_dump = true;
        if (need_dump) {
            char name[64];
            if (gba && gba->cpu)
                printf("frame %d pc=%08X cpsr=%08X keys=%04X\n", frame, gba->cpu->gprs[15] & ~1u, gba->cpu->cpsr.packed, keys);
            else
                printf("frame %d\n", frame);
            snprintf(name, sizeof(name), "vram_%04d", frame); dump_region(core, 0x06000000, 0x18000, outdir, name);
            snprintf(name, sizeof(name), "ewram_%04d", frame); dump_region(core, 0x02000000, 0x40000, outdir, name);
            snprintf(name, sizeof(name), "iwram_%04d", frame); dump_region(core, 0x03000000, 0x8000, outdir, name);
            snprintf(name, sizeof(name), "pal_%04d", frame); dump_region(core, 0x05000000, 0x400, outdir, name);
            snprintf(name, sizeof(name), "oam_%04d", frame); dump_region(core, 0x07000000, 0x400, outdir, name);
            snprintf(name, sizeof(name), "io_%04d", frame); dump_region(core, 0x04000000, 0x400, outdir, name);
            snprintf(name, sizeof(name), "shot_%04d", frame); write_ppm(vbuf, outdir, name);
        }
    }
    dump_region(core, 0x0E000000, 0x8000, outdir, "sram");
    core->deinit(core);
    free(vbuf);
    return 0;
}
