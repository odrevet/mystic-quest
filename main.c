#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include <quickjs/quickjs.h>

JSValue text(JSContext *ctx, JSValueConst jsThis, int argc, JSValueConst *argv)
{
    const char *str = JS_ToCString(ctx, argv[0]);
    puts(str);
    return JS_UNDEFINED;
}

JSValue cond_flags(JSContext *ctx, JSValueConst jsThis, int argc, JSValueConst *argv)
{
    const char *str = JS_ToCString(ctx, argv[0]);
    puts(str);
    // return JS_FALSE;
    return JS_TRUE;
}

void initContext(JSContext *ctx)
{
    JSValue global = JS_GetGlobalObject(ctx);
    JS_SetPropertyStr(ctx, global, "text", JS_NewCFunction(ctx, text, "text", 1));
    JS_SetPropertyStr(ctx, global, "cond_flags", JS_NewCFunction(ctx, cond_flags, "cond_flags", 1));
    JS_FreeValue(ctx, global);
}

char *readfile(char *file_name)
{
    FILE *fp;
    long lSize;
    char *buffer;

    // Read file content into buffer
    fp = fopen(file_name, "rb");
    if (!fp)
        perror(file_name), exit(1);

    fseek(fp, 0L, SEEK_END);
    lSize = ftell(fp);
    rewind(fp);

    buffer = calloc(1, lSize + 1);
    if (!buffer)
        fclose(fp), fputs("memory alloc fails", stderr), exit(1);

    if (1 != fread(buffer, lSize, 1, fp))
        fclose(fp), free(buffer), fputs("entire read fails", stderr), exit(1);

    fclose(fp);
    return buffer;
}

int main(int argc, char *argv[])
{
    char *file_name = argv[1];
    char *function_name = argv[2];

    char *buffer = readfile(file_name);

    // QJS runtime
    JSRuntime *rt = JS_NewRuntime();
    JSContext *ctx = JS_NewContext(rt);

    initContext(ctx);

    if (JS_IsException(JS_Eval(ctx, buffer, strlen(buffer), "<input>", JS_EVAL_FLAG_STRICT)))
    {
        JSValue e = JS_GetException(ctx);
        JS_FreeContext(ctx);
        JS_FreeRuntime(rt);
        free(buffer);
        return -1;
    }
    free(buffer);

    JSValue global = JS_GetGlobalObject(ctx);
    JSValue function = JS_GetPropertyStr(ctx, global, function_name);
    JSValue jsResult = JS_Call(ctx, function, global, 0, NULL);

    if (JS_IsException(jsResult))
    {
        printf("ERROR...\n");
        return 0;
    }

    // Free memory
    JSValue used[] = {jsResult, function, global};
    for (int i = 0; i < sizeof(used) / sizeof(JSValue); ++i)
    {
        JS_FreeValue(ctx, used[i]);
    }

    JS_FreeContext(ctx);
    JS_FreeRuntime(rt);

    return 0;
}
