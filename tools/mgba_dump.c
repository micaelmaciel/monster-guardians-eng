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
#include <mgba/internal/gba/input.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>

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
    core->reset(core);

    color_t* vbuf = calloc(240 * 160, sizeof(color_t));
    core->setVideoBuffer(core, vbuf, 240);
    /* Associate the software renderer now that an output buffer exists. */
    core->reloadConfigOption(core, "hwaccelVideo", &core->config);

    /* parse dump frames */
    int frames[64]; int nframes = 0;
    { char* tmp = strdup(frames_csv); char* tok = strtok(tmp, ",");
      while (tok && nframes < 64) { frames[nframes++] = atoi(tok); tok = strtok(NULL, ","); } free(tmp); }
    int maxframe = 0;
    for (int i = 0; i < nframes; i++) if (frames[i] > maxframe) maxframe = frames[i];

    /* parse input windows */
    struct { int a, b; uint32_t keys; } inputs[32]; int nin = 0;
    { char* tmp = strdup(input_spec); char* tok = strtok(tmp, ",");
      while (tok && nin < 32) {
        char* colon = strchr(tok, ':');
        if (colon) { *colon = 0;
            int a = 0, b = 0;
            if (sscanf(tok, "%d-%d", &a, &b) < 2) { a = b = atoi(tok); }
            uint32_t keys = 0; char* k = strtok(colon + 1, "+");
            while (k) { keys |= keybit(k); k = strtok(NULL, "+"); }
            inputs[nin].a = a; inputs[nin].b = b; inputs[nin].keys = keys; nin++;
        }
        tok = strtok(NULL, ","); } free(tmp); }

    for (int frame = 0; frame <= maxframe; frame++) {
        uint32_t keys = 0;
        for (int i = 0; i < nin; i++)
            if (frame >= inputs[i].a && frame <= inputs[i].b) keys |= inputs[i].keys;
        core->setKeys(core, keys);
        core->runFrame(core);
        bool need_dump = false;
        for (int i = 0; i < nframes; i++) if (frames[i] == frame) need_dump = true;
        if (need_dump) {
            char name[64];
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
    core->deinit(core);
    free(vbuf);
    return 0;
}
