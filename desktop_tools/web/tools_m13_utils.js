/* 工具箱（M13）cURL 解析工具
 *
 * 设计目标：
 * - 纯算法、无 DOM 依赖
 * - 解析 cURL 命令提取请求信息
 * - 生成多语言代码片段
 */
(function (root, factory) {
    if (typeof module !== 'undefined' && module.exports) {
        module.exports = factory();
    } else {
        root.DogToolboxM13Utils = factory();
    }
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
    'use strict';

    /**
     * 解析 cURL 命令
     * @param {string} curlCommand - cURL 命令字符串
     * @returns {{url: string, method: string, headers: Object, data: string|null, errors: string[]}}
     */
    function parseCurl(curlCommand) {
        const result = {
            url: '',
            method: 'GET',
            headers: {},
            data: null,
            cookies: {},
            auth: null,
            insecure: false,
            compressed: false,
            errors: []
        };

        if (!curlCommand || typeof curlCommand !== 'string') {
            result.errors.push('无效的 cURL 命令');
            return result;
        }

        // 规范化：移除换行续行符、合并多行
        let cmd = curlCommand
            .replace(/\\\r?\n/g, ' ')
            .replace(/\r?\n/g, ' ')
            .trim();

        // 检查是否以 curl 开头
        if (!/^curl\s/i.test(cmd)) {
            result.errors.push('命令必须以 curl 开头');
            return result;
        }

        // 移除 curl 前缀
        cmd = cmd.replace(/^curl\s+/i, '');

        // 分词（处理引号）
        const tokens = tokenize(cmd);

        let i = 0;
        while (i < tokens.length) {
            const token = tokens[i];

            // -X, --request: HTTP 方法
            if (token === '-X' || token === '--request') {
                if (i + 1 < tokens.length) {
                    result.method = tokens[++i].toUpperCase();
                }
            }
            // -H, --header: 请求头
            else if (token === '-H' || token === '--header') {
                if (i + 1 < tokens.length) {
                    const header = tokens[++i];
                    const colonIdx = header.indexOf(':');
                    if (colonIdx > 0) {
                        const key = header.slice(0, colonIdx).trim();
                        const value = header.slice(colonIdx + 1).trim();
                        result.headers[key] = value;
                    }
                }
            }
            // -d, --data, --data-raw, --data-binary: 请求体
            else if (token === '-d' || token === '--data' || token === '--data-raw' || token === '--data-binary') {
                if (i + 1 < tokens.length) {
                    result.data = tokens[++i];
                    // 有 data 默认 POST
                    if (result.method === 'GET') {
                        result.method = 'POST';
                    }
                }
            }
            // --data-urlencode
            else if (token === '--data-urlencode') {
                if (i + 1 < tokens.length) {
                    const encoded = tokens[++i];
                    if (result.data) {
                        result.data += '&' + encodeURIComponent(encoded);
                    } else {
                        result.data = encodeURIComponent(encoded);
                    }
                    if (result.method === 'GET') {
                        result.method = 'POST';
                    }
                }
            }
            // -b, --cookie: Cookie
            else if (token === '-b' || token === '--cookie') {
                if (i + 1 < tokens.length) {
                    const cookieStr = tokens[++i];
                    parseCookieString(cookieStr, result.cookies);
                }
            }
            // -u, --user: 认证
            else if (token === '-u' || token === '--user') {
                if (i + 1 < tokens.length) {
                    result.auth = tokens[++i];
                }
            }
            // -k, --insecure: 忽略 SSL
            else if (token === '-k' || token === '--insecure') {
                result.insecure = true;
            }
            // --compressed
            else if (token === '--compressed') {
                result.compressed = true;
            }
            // -A, --user-agent
            else if (token === '-A' || token === '--user-agent') {
                if (i + 1 < tokens.length) {
                    result.headers['User-Agent'] = tokens[++i];
                }
            }
            // -e, --referer
            else if (token === '-e' || token === '--referer') {
                if (i + 1 < tokens.length) {
                    result.headers['Referer'] = tokens[++i];
                }
            }
            // --json: JSON 数据（自动设置 Content-Type）
            else if (token === '--json') {
                if (i + 1 < tokens.length) {
                    result.data = tokens[++i];
                    result.headers['Content-Type'] = 'application/json';
                    result.headers['Accept'] = 'application/json';
                    if (result.method === 'GET') {
                        result.method = 'POST';
                    }
                }
            }
            // -F, --form: 表单数据
            else if (token === '-F' || token === '--form') {
                if (i + 1 < tokens.length) {
                    // 简化处理，仅标记为 multipart
                    if (!result.formData) {
                        result.formData = [];
                    }
                    result.formData.push(tokens[++i]);
                    if (result.method === 'GET') {
                        result.method = 'POST';
                    }
                }
            }
            // URL（不以 - 开头的非选项参数）
            else if (!token.startsWith('-') && !result.url) {
                result.url = token;
            }
            // 忽略的选项（带参数）
            else if (['-o', '--output', '-O', '--remote-name', '-L', '--location',
                      '-s', '--silent', '-S', '--show-error', '-v', '--verbose',
                      '-I', '--head', '-G', '--get', '--connect-timeout', '--max-time'].includes(token)) {
                // 有些需要跳过参数
                if (['--connect-timeout', '--max-time', '-o', '--output'].includes(token)) {
                    i++;
                }
                // -I/--head 改变方法
                if (token === '-I' || token === '--head') {
                    result.method = 'HEAD';
                }
                // -G/--get 强制 GET
                if (token === '-G' || token === '--get') {
                    result.method = 'GET';
                }
            }

            i++;
        }

        // 验证
        if (!result.url) {
            result.errors.push('未找到 URL');
        }

        return result;
    }

    /**
     * 分词（处理单引号、双引号、$'...' 形式）
     */
    function tokenize(str) {
        const tokens = [];
        let i = 0;
        const len = str.length;

        while (i < len) {
            // 跳过空白
            while (i < len && /\s/.test(str[i])) i++;
            if (i >= len) break;

            let token = '';

            // $'...' 形式（bash ANSI-C 引用）
            if (str[i] === '$' && i + 1 < len && str[i + 1] === "'") {
                i += 2;
                while (i < len && str[i] !== "'") {
                    if (str[i] === '\\' && i + 1 < len) {
                        const next = str[i + 1];
                        if (next === 'n') { token += '\n'; i += 2; }
                        else if (next === 'r') { token += '\r'; i += 2; }
                        else if (next === 't') { token += '\t'; i += 2; }
                        else if (next === '\\') { token += '\\'; i += 2; }
                        else if (next === "'") { token += "'"; i += 2; }
                        else { token += str[i]; i++; }
                    } else {
                        token += str[i++];
                    }
                }
                i++; // 跳过结束引号
            }
            // 单引号
            else if (str[i] === "'") {
                i++;
                while (i < len && str[i] !== "'") {
                    token += str[i++];
                }
                i++; // 跳过结束引号
            }
            // 双引号
            else if (str[i] === '"') {
                i++;
                while (i < len && str[i] !== '"') {
                    if (str[i] === '\\' && i + 1 < len) {
                        const next = str[i + 1];
                        if (next === '"' || next === '\\' || next === '$' || next === '`') {
                            token += next;
                            i += 2;
                        } else if (next === 'n') {
                            token += '\n';
                            i += 2;
                        } else {
                            token += str[i++];
                        }
                    } else {
                        token += str[i++];
                    }
                }
                i++; // 跳过结束引号
            }
            // 普通 token
            else {
                while (i < len && !/\s/.test(str[i])) {
                    if (str[i] === '\\' && i + 1 < len) {
                        token += str[i + 1];
                        i += 2;
                    } else {
                        token += str[i++];
                    }
                }
            }

            if (token) {
                tokens.push(token);
            }
        }

        return tokens;
    }

    /**
     * 解析 Cookie 字符串
     */
    function parseCookieString(cookieStr, target) {
        if (!cookieStr) return;
        const pairs = cookieStr.split(';');
        for (const pair of pairs) {
            const eqIdx = pair.indexOf('=');
            if (eqIdx > 0) {
                const key = pair.slice(0, eqIdx).trim();
                const value = pair.slice(eqIdx + 1).trim();
                target[key] = value;
            }
        }
    }

    /**
     * 生成 JavaScript Fetch 代码
     */
    function toFetch(parsed) {
        const lines = [];
        const options = {};

        if (parsed.method !== 'GET') {
            options.method = parsed.method;
        }

        const hasHeaders = Object.keys(parsed.headers).length > 0;
        const hasCookies = Object.keys(parsed.cookies).length > 0;

        if (hasHeaders || hasCookies) {
            options.headers = { ...parsed.headers };
            if (hasCookies) {
                const cookieStr = Object.entries(parsed.cookies)
                    .map(([k, v]) => `${k}=${v}`)
                    .join('; ');
                options.headers['Cookie'] = cookieStr;
            }
        }

        if (parsed.data) {
            options.body = parsed.data;
        }

        lines.push(`fetch('${escapeJs(parsed.url)}'${Object.keys(options).length ? ', {' : ')'}`);

        if (Object.keys(options).length) {
            if (options.method) {
                lines.push(`  method: '${options.method}',`);
            }
            if (options.headers) {
                lines.push('  headers: {');
                for (const [k, v] of Object.entries(options.headers)) {
                    lines.push(`    '${escapeJs(k)}': '${escapeJs(v)}',`);
                }
                lines.push('  },');
            }
            if (options.body) {
                const isJson = tryParseJson(options.body);
                if (isJson) {
                    lines.push(`  body: JSON.stringify(${options.body}),`);
                } else {
                    lines.push(`  body: '${escapeJs(options.body)}',`);
                }
            }
            lines.push('})');
        }

        lines.push('.then(response => response.json())');
        lines.push('.then(data => console.log(data))');
        lines.push('.catch(error => console.error(error));');

        return lines.join('\n');
    }

    /**
     * 生成 JavaScript Axios 代码
     */
    function toAxios(parsed) {
        const lines = [];
        const config = {
            url: parsed.url,
            method: parsed.method.toLowerCase()
        };

        const hasHeaders = Object.keys(parsed.headers).length > 0;
        const hasCookies = Object.keys(parsed.cookies).length > 0;

        if (hasHeaders || hasCookies) {
            config.headers = { ...parsed.headers };
            if (hasCookies) {
                const cookieStr = Object.entries(parsed.cookies)
                    .map(([k, v]) => `${k}=${v}`)
                    .join('; ');
                config.headers['Cookie'] = cookieStr;
            }
        }

        if (parsed.data) {
            config.data = parsed.data;
        }

        lines.push('axios({');
        lines.push(`  method: '${config.method}',`);
        lines.push(`  url: '${escapeJs(config.url)}',`);

        if (config.headers) {
            lines.push('  headers: {');
            for (const [k, v] of Object.entries(config.headers)) {
                lines.push(`    '${escapeJs(k)}': '${escapeJs(v)}',`);
            }
            lines.push('  },');
        }

        if (config.data) {
            const isJson = tryParseJson(config.data);
            if (isJson) {
                lines.push(`  data: ${config.data},`);
            } else {
                lines.push(`  data: '${escapeJs(config.data)}',`);
            }
        }

        lines.push('})');
        lines.push('.then(response => console.log(response.data))');
        lines.push('.catch(error => console.error(error));');

        return lines.join('\n');
    }

    /**
     * 生成 Python requests 代码
     */
    function toPythonRequests(parsed) {
        const lines = [];
        lines.push('import requests');
        lines.push('');

        const hasHeaders = Object.keys(parsed.headers).length > 0;
        const hasCookies = Object.keys(parsed.cookies).length > 0;

        if (hasHeaders) {
            lines.push('headers = {');
            for (const [k, v] of Object.entries(parsed.headers)) {
                lines.push(`    '${escapePy(k)}': '${escapePy(v)}',`);
            }
            lines.push('}');
            lines.push('');
        }

        if (hasCookies) {
            lines.push('cookies = {');
            for (const [k, v] of Object.entries(parsed.cookies)) {
                lines.push(`    '${escapePy(k)}': '${escapePy(v)}',`);
            }
            lines.push('}');
            lines.push('');
        }

        if (parsed.data) {
            const isJson = tryParseJson(parsed.data);
            if (isJson) {
                lines.push(`data = ${parsed.data}`);
            } else {
                lines.push(`data = '${escapePy(parsed.data)}'`);
            }
            lines.push('');
        }

        const method = parsed.method.toLowerCase();
        let call = `response = requests.${method}('${escapePy(parsed.url)}'`;

        const params = [];
        if (hasHeaders) params.push('headers=headers');
        if (hasCookies) params.push('cookies=cookies');
        if (parsed.data) {
            const isJson = tryParseJson(parsed.data);
            params.push(isJson ? 'json=data' : 'data=data');
        }
        if (parsed.auth) {
            const [user, pass] = parsed.auth.split(':');
            params.push(`auth=('${escapePy(user || '')}', '${escapePy(pass || '')}')`);
        }
        if (parsed.insecure) {
            params.push('verify=False');
        }

        if (params.length) {
            call += ', ' + params.join(', ');
        }
        call += ')';

        lines.push(call);
        lines.push('');
        lines.push('print(response.status_code)');
        lines.push('print(response.text)');

        return lines.join('\n');
    }

    /**
     * 生成 Node.js http/https 代码
     */
    function toNodeHttp(parsed) {
        const lines = [];
        const isHttps = parsed.url.startsWith('https');
        const mod = isHttps ? 'https' : 'http';

        lines.push(`const ${mod} = require('${mod}');`);
        lines.push('');

        lines.push('const options = {');

        // 解析 URL
        try {
            const url = new URL(parsed.url);
            lines.push(`  hostname: '${escapeJs(url.hostname)}',`);
            if (url.port) {
                lines.push(`  port: ${url.port},`);
            }
            lines.push(`  path: '${escapeJs(url.pathname + url.search)}',`);
        } catch (e) {
            lines.push(`  // URL 解析失败: ${parsed.url}`);
        }

        lines.push(`  method: '${parsed.method}',`);

        const hasHeaders = Object.keys(parsed.headers).length > 0;
        if (hasHeaders) {
            lines.push('  headers: {');
            for (const [k, v] of Object.entries(parsed.headers)) {
                lines.push(`    '${escapeJs(k)}': '${escapeJs(v)}',`);
            }
            lines.push('  },');
        }

        lines.push('};');
        lines.push('');

        lines.push(`const req = ${mod}.request(options, (res) => {`);
        lines.push('  let data = \'\';');
        lines.push('  res.on(\'data\', chunk => data += chunk);');
        lines.push('  res.on(\'end\', () => console.log(data));');
        lines.push('});');
        lines.push('');
        lines.push('req.on(\'error\', error => console.error(error));');

        if (parsed.data) {
            lines.push('');
            lines.push(`req.write('${escapeJs(parsed.data)}');`);
        }

        lines.push('req.end();');

        return lines.join('\n');
    }

    /**
     * 生成 PHP cURL 代码
     */
    function toPhpCurl(parsed) {
        const lines = [];
        lines.push('<?php');
        lines.push('$ch = curl_init();');
        lines.push('');
        lines.push(`curl_setopt($ch, CURLOPT_URL, '${escapePhp(parsed.url)}');`);
        lines.push('curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);');

        if (parsed.method !== 'GET') {
            lines.push(`curl_setopt($ch, CURLOPT_CUSTOMREQUEST, '${parsed.method}');`);
        }

        const hasHeaders = Object.keys(parsed.headers).length > 0;
        if (hasHeaders) {
            lines.push('');
            lines.push('$headers = array(');
            for (const [k, v] of Object.entries(parsed.headers)) {
                lines.push(`    '${escapePhp(k)}: ${escapePhp(v)}',`);
            }
            lines.push(');');
            lines.push('curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);');
        }

        if (parsed.data) {
            lines.push('');
            lines.push(`curl_setopt($ch, CURLOPT_POSTFIELDS, '${escapePhp(parsed.data)}');`);
        }

        if (parsed.insecure) {
            lines.push('');
            lines.push('curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);');
        }

        lines.push('');
        lines.push('$response = curl_exec($ch);');
        lines.push('curl_close($ch);');
        lines.push('');
        lines.push('echo $response;');
        lines.push('?>');

        return lines.join('\n');
    }

    /**
     * 生成 Go 代码
     */
    function toGo(parsed) {
        const lines = [];
        lines.push('package main');
        lines.push('');
        lines.push('import (');
        lines.push('    "fmt"');
        lines.push('    "io/ioutil"');
        lines.push('    "net/http"');
        if (parsed.data) {
            lines.push('    "strings"');
        }
        lines.push(')');
        lines.push('');
        lines.push('func main() {');

        if (parsed.data) {
            lines.push(`    body := strings.NewReader(\`${parsed.data}\`)`);
            lines.push(`    req, err := http.NewRequest("${parsed.method}", "${escapeGo(parsed.url)}", body)`);
        } else {
            lines.push(`    req, err := http.NewRequest("${parsed.method}", "${escapeGo(parsed.url)}", nil)`);
        }

        lines.push('    if err != nil {');
        lines.push('        panic(err)');
        lines.push('    }');

        const hasHeaders = Object.keys(parsed.headers).length > 0;
        if (hasHeaders) {
            lines.push('');
            for (const [k, v] of Object.entries(parsed.headers)) {
                lines.push(`    req.Header.Set("${escapeGo(k)}", "${escapeGo(v)}")`);
            }
        }

        lines.push('');
        lines.push('    client := &http.Client{}');
        lines.push('    resp, err := client.Do(req)');
        lines.push('    if err != nil {');
        lines.push('        panic(err)');
        lines.push('    }');
        lines.push('    defer resp.Body.Close()');
        lines.push('');
        lines.push('    respBody, _ := ioutil.ReadAll(resp.Body)');
        lines.push('    fmt.Println(string(respBody))');
        lines.push('}');

        return lines.join('\n');
    }

    // 辅助函数
    function escapeJs(str) {
        return String(str || '')
            .replace(/\\/g, '\\\\')
            .replace(/'/g, "\\'")
            .replace(/\n/g, '\\n')
            .replace(/\r/g, '\\r');
    }

    function escapePy(str) {
        return String(str || '')
            .replace(/\\/g, '\\\\')
            .replace(/'/g, "\\'")
            .replace(/\n/g, '\\n')
            .replace(/\r/g, '\\r');
    }

    function escapePhp(str) {
        return String(str || '')
            .replace(/\\/g, '\\\\')
            .replace(/'/g, "\\'")
            .replace(/\n/g, '\\n');
    }

    function escapeGo(str) {
        return String(str || '')
            .replace(/\\/g, '\\\\')
            .replace(/"/g, '\\"')
            .replace(/\n/g, '\\n');
    }

    function tryParseJson(str) {
        if (!str) return false;
        const trimmed = String(str).trim();
        if ((trimmed.startsWith('{') && trimmed.endsWith('}')) ||
            (trimmed.startsWith('[') && trimmed.endsWith(']'))) {
            try {
                JSON.parse(trimmed);
                return true;
            } catch (e) {
                return false;
            }
        }
        return false;
    }

    /**
     * 格式化解析结果为可读文本
     */
    function formatParsedResult(parsed) {
        const lines = [];
        lines.push(`方法: ${parsed.method}`);
        lines.push(`URL: ${parsed.url}`);

        if (Object.keys(parsed.headers).length > 0) {
            lines.push('');
            lines.push('请求头:');
            for (const [k, v] of Object.entries(parsed.headers)) {
                lines.push(`  ${k}: ${v}`);
            }
        }

        if (Object.keys(parsed.cookies).length > 0) {
            lines.push('');
            lines.push('Cookies:');
            for (const [k, v] of Object.entries(parsed.cookies)) {
                lines.push(`  ${k}=${v}`);
            }
        }

        if (parsed.data) {
            lines.push('');
            lines.push('请求体:');
            // 尝试格式化 JSON
            if (tryParseJson(parsed.data)) {
                try {
                    const obj = JSON.parse(parsed.data);
                    lines.push(JSON.stringify(obj, null, 2));
                } catch (e) {
                    lines.push(parsed.data);
                }
            } else {
                lines.push(parsed.data);
            }
        }

        if (parsed.auth) {
            lines.push('');
            lines.push(`认证: ${parsed.auth}`);
        }

        if (parsed.insecure) {
            lines.push('');
            lines.push('⚠ 忽略 SSL 证书验证');
        }

        return lines.join('\n');
    }

    return {
        parseCurl,
        toFetch,
        toAxios,
        toPythonRequests,
        toNodeHttp,
        toPhpCurl,
        toGo,
        formatParsedResult
    };
});
