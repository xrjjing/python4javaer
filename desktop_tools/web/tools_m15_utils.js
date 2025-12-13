/* 工具箱（M15）IP/Cron/SQL 工具
 *
 * 设计目标：
 * - 纯算法、无 DOM 依赖
 * - IP 地址验证与转换、子网计算
 * - Cron 表达式解析与描述
 * - SQL 格式化美化
 */
(function (root, factory) {
    if (typeof module !== 'undefined' && module.exports) {
        module.exports = factory();
    } else {
        root.DogToolboxM15Utils = factory();
    }
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
    'use strict';

    // ========== IP 工具 ==========

    /**
     * 验证 IPv4 地址
     */
    function isValidIPv4(ip) {
        if (!ip || typeof ip !== 'string') return false;
        const parts = ip.split('.');
        if (parts.length !== 4) return false;
        return parts.every(part => {
            if (!/^\d+$/.test(part)) return false;
            const num = parseInt(part, 10);
            return num >= 0 && num <= 255 && String(num) === part;
        });
    }

    /**
     * 验证 IPv6 地址（简化版）
     */
    function isValidIPv6(ip) {
        if (!ip || typeof ip !== 'string') return false;
        // 简化验证：检查格式
        const fullPattern = /^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$/;
        const compressedPattern = /^(([0-9a-fA-F]{1,4}:)*)?::([0-9a-fA-F]{1,4}:)*[0-9a-fA-F]{1,4}$|^::$/;
        return fullPattern.test(ip) || compressedPattern.test(ip) || /^([0-9a-fA-F]{1,4}:){1,7}:$/.test(ip);
    }

    /**
     * IPv4 转十进制
     */
    function ipv4ToDecimal(ip) {
        if (!isValidIPv4(ip)) return null;
        const parts = ip.split('.').map(p => parseInt(p, 10));
        return ((parts[0] << 24) >>> 0) + (parts[1] << 16) + (parts[2] << 8) + parts[3];
    }

    /**
     * 十进制转 IPv4
     */
    function decimalToIPv4(num) {
        if (typeof num !== 'number' || num < 0 || num > 4294967295) return null;
        return [
            (num >>> 24) & 255,
            (num >>> 16) & 255,
            (num >>> 8) & 255,
            num & 255
        ].join('.');
    }

    /**
     * IPv4 转十六进制
     */
    function ipv4ToHex(ip) {
        const dec = ipv4ToDecimal(ip);
        if (dec === null) return null;
        return '0x' + dec.toString(16).padStart(8, '0').toUpperCase();
    }

    /**
     * IPv4 转二进制
     */
    function ipv4ToBinary(ip) {
        if (!isValidIPv4(ip)) return null;
        return ip.split('.').map(p => parseInt(p, 10).toString(2).padStart(8, '0')).join('.');
    }

    /**
     * 解析 CIDR 表示法
     */
    function parseCIDR(cidr) {
        if (!cidr || typeof cidr !== 'string') {
            return { error: '无效的 CIDR 输入' };
        }

        const match = cidr.match(/^(\d+\.\d+\.\d+\.\d+)\/(\d+)$/);
        if (!match) {
            return { error: '无效的 CIDR 格式，应为 x.x.x.x/n' };
        }

        const ip = match[1];
        const prefix = parseInt(match[2], 10);

        if (!isValidIPv4(ip)) {
            return { error: '无效的 IP 地址' };
        }

        if (prefix < 0 || prefix > 32) {
            return { error: '子网前缀必须在 0-32 之间' };
        }

        const ipDec = ipv4ToDecimal(ip);
        const mask = prefix === 0 ? 0 : (~0 << (32 - prefix)) >>> 0;
        const networkDec = (ipDec & mask) >>> 0;
        const broadcastDec = (networkDec | (~mask >>> 0)) >>> 0;
        const hostCount = prefix >= 31 ? (prefix === 32 ? 1 : 2) : Math.pow(2, 32 - prefix) - 2;

        return {
            ip: ip,
            prefix: prefix,
            netmask: decimalToIPv4(mask),
            network: decimalToIPv4(networkDec),
            broadcast: decimalToIPv4(broadcastDec),
            firstHost: prefix >= 31 ? decimalToIPv4(networkDec) : decimalToIPv4(networkDec + 1),
            lastHost: prefix >= 31 ? decimalToIPv4(broadcastDec) : decimalToIPv4(broadcastDec - 1),
            hostCount: hostCount,
            ipClass: getIPClass(ip),
            isPrivate: isPrivateIP(ip)
        };
    }

    /**
     * 获取 IP 类别
     */
    function getIPClass(ip) {
        if (!isValidIPv4(ip)) return null;
        const first = parseInt(ip.split('.')[0], 10);
        if (first >= 1 && first <= 126) return 'A';
        if (first >= 128 && first <= 191) return 'B';
        if (first >= 192 && first <= 223) return 'C';
        if (first >= 224 && first <= 239) return 'D (组播)';
        if (first >= 240 && first <= 255) return 'E (保留)';
        return '特殊';
    }

    /**
     * 判断是否为私有 IP
     */
    function isPrivateIP(ip) {
        if (!isValidIPv4(ip)) return false;
        const parts = ip.split('.').map(p => parseInt(p, 10));
        // 10.0.0.0/8
        if (parts[0] === 10) return true;
        // 172.16.0.0/12
        if (parts[0] === 172 && parts[1] >= 16 && parts[1] <= 31) return true;
        // 192.168.0.0/16
        if (parts[0] === 192 && parts[1] === 168) return true;
        return false;
    }

    // ========== Cron 表达式解析 ==========

    const CRON_FIELDS = ['minute', 'hour', 'dayOfMonth', 'month', 'dayOfWeek'];
    const CRON_RANGES = {
        minute: { min: 0, max: 59 },
        hour: { min: 0, max: 23 },
        dayOfMonth: { min: 1, max: 31 },
        month: { min: 1, max: 12 },
        dayOfWeek: { min: 0, max: 7 }  // 0 和 7 都表示周日
    };

    const MONTH_NAMES = ['', '一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月'];
    const DAY_NAMES = ['周日', '周一', '周二', '周三', '周四', '周五', '周六', '周日'];

    /**
     * 解析 Cron 表达式
     */
    function parseCron(expression) {
        if (!expression || typeof expression !== 'string') {
            return { error: '无效的 Cron 表达式' };
        }

        const parts = expression.trim().split(/\s+/);
        if (parts.length < 5 || parts.length > 6) {
            return { error: 'Cron 表达式应为 5 或 6 个字段' };
        }

        // 如果是 6 字段，第一个是秒（忽略）
        const fields = parts.length === 6 ? parts.slice(1) : parts;
        const parsed = {};
        const descriptions = [];

        try {
            for (let i = 0; i < 5; i++) {
                const field = CRON_FIELDS[i];
                const value = fields[i];
                const range = CRON_RANGES[field];

                parsed[field] = parseField(value, range.min, range.max);
                descriptions.push(describeField(field, value, parsed[field]));
            }
        } catch (e) {
            return { error: e.message };
        }

        return {
            expression: expression,
            parsed: parsed,
            description: buildDescription(descriptions, parsed),
            nextRuns: calculateNextRuns(parsed, 5)
        };
    }

    /**
     * 解析单个字段
     */
    function parseField(value, min, max) {
        if (value === '*') {
            return { type: 'all' };
        }

        // */n 格式
        if (value.startsWith('*/')) {
            const step = parseInt(value.slice(2), 10);
            if (isNaN(step) || step < 1) throw new Error(`无效的步长: ${value}`);
            return { type: 'step', step: step, from: min };
        }

        // 范围 n-m
        if (value.includes('-') && !value.includes(',')) {
            const [start, end] = value.split('-').map(v => parseInt(v, 10));
            if (isNaN(start) || isNaN(end)) throw new Error(`无效的范围: ${value}`);
            if (start < min || end > max || start > end) throw new Error(`范围超出限制: ${value}`);
            return { type: 'range', from: start, to: end };
        }

        // 列表 n,m,o
        if (value.includes(',')) {
            const values = value.split(',').map(v => {
                const num = parseInt(v.trim(), 10);
                if (isNaN(num) || num < min || num > max) throw new Error(`无效的值: ${v}`);
                return num;
            });
            return { type: 'list', values: values };
        }

        // 单个值
        const num = parseInt(value, 10);
        if (isNaN(num) || num < min || num > max) throw new Error(`无效的值: ${value}`);
        return { type: 'value', value: num };
    }

    /**
     * 描述单个字段
     */
    function describeField(field, rawValue, parsed) {
        if (parsed.type === 'all') return null;

        switch (field) {
            case 'minute':
                if (parsed.type === 'value') return `第 ${parsed.value} 分钟`;
                if (parsed.type === 'step') return `每 ${parsed.step} 分钟`;
                if (parsed.type === 'range') return `第 ${parsed.from}-${parsed.to} 分钟`;
                if (parsed.type === 'list') return `第 ${parsed.values.join(', ')} 分钟`;
                break;
            case 'hour':
                if (parsed.type === 'value') return `${parsed.value} 点`;
                if (parsed.type === 'step') return `每 ${parsed.step} 小时`;
                if (parsed.type === 'range') return `${parsed.from}-${parsed.to} 点`;
                if (parsed.type === 'list') return `${parsed.values.join(', ')} 点`;
                break;
            case 'dayOfMonth':
                if (parsed.type === 'value') return `每月 ${parsed.value} 日`;
                if (parsed.type === 'step') return `每 ${parsed.step} 天`;
                if (parsed.type === 'range') return `每月 ${parsed.from}-${parsed.to} 日`;
                if (parsed.type === 'list') return `每月 ${parsed.values.join(', ')} 日`;
                break;
            case 'month':
                if (parsed.type === 'value') return MONTH_NAMES[parsed.value];
                if (parsed.type === 'step') return `每 ${parsed.step} 个月`;
                if (parsed.type === 'range') return `${MONTH_NAMES[parsed.from]}-${MONTH_NAMES[parsed.to]}`;
                if (parsed.type === 'list') return parsed.values.map(v => MONTH_NAMES[v]).join(', ');
                break;
            case 'dayOfWeek':
                if (parsed.type === 'value') return DAY_NAMES[parsed.value % 7];
                if (parsed.type === 'range') return `${DAY_NAMES[parsed.from]}-${DAY_NAMES[parsed.to % 7]}`;
                if (parsed.type === 'list') return parsed.values.map(v => DAY_NAMES[v % 7]).join(', ');
                break;
        }
        return rawValue;
    }

    /**
     * 构建人类可读描述
     */
    function buildDescription(descriptions, parsed) {
        const parts = [];

        // 时间部分
        const minute = parsed.minute;
        const hour = parsed.hour;

        if (minute.type === 'all' && hour.type === 'all') {
            parts.push('每分钟');
        } else if (minute.type === 'step' && hour.type === 'all') {
            parts.push(`每 ${minute.step} 分钟`);
        } else if (minute.type === 'value' && hour.type === 'all') {
            parts.push(`每小时第 ${minute.value} 分钟`);
        } else if (minute.type === 'value' && hour.type === 'value') {
            parts.push(`${hour.value}:${String(minute.value).padStart(2, '0')}`);
        } else if (minute.type === 'value' && hour.type === 'step') {
            parts.push(`每 ${hour.step} 小时的第 ${minute.value} 分钟`);
        } else {
            if (descriptions[1]) parts.push(descriptions[1]);
            if (descriptions[0]) parts.push(descriptions[0]);
        }

        // 日期部分
        const dom = parsed.dayOfMonth;
        const month = parsed.month;
        const dow = parsed.dayOfWeek;

        if (dom.type !== 'all' && descriptions[2]) {
            parts.push(descriptions[2]);
        }
        if (month.type !== 'all' && descriptions[3]) {
            parts.push(descriptions[3]);
        }
        if (dow.type !== 'all' && descriptions[4]) {
            parts.push(descriptions[4]);
        }

        return parts.length > 0 ? parts.join('，') : '每分钟执行';
    }

    /**
     * 计算下次运行时间
     */
    function calculateNextRuns(parsed, count) {
        const runs = [];
        const now = new Date();
        let current = new Date(now);
        current.setSeconds(0, 0);

        for (let i = 0; i < 1000 && runs.length < count; i++) {
            current = new Date(current.getTime() + 60000);
            if (matchesCron(current, parsed)) {
                runs.push(formatDateTime(current));
            }
        }

        return runs;
    }

    /**
     * 检查时间是否匹配 Cron
     */
    function matchesCron(date, parsed) {
        const minute = date.getMinutes();
        const hour = date.getHours();
        const dom = date.getDate();
        const month = date.getMonth() + 1;
        const dow = date.getDay();

        return matchesField(minute, parsed.minute) &&
               matchesField(hour, parsed.hour) &&
               matchesField(dom, parsed.dayOfMonth) &&
               matchesField(month, parsed.month) &&
               matchesField(dow, parsed.dayOfWeek);
    }

    /**
     * 检查值是否匹配字段
     */
    function matchesField(value, field) {
        switch (field.type) {
            case 'all': return true;
            case 'value': return value === field.value || (field.value === 7 && value === 0);
            case 'step': return value % field.step === 0;
            case 'range': return value >= field.from && value <= field.to;
            case 'list': return field.values.includes(value) || (field.values.includes(7) && value === 0);
            default: return false;
        }
    }

    /**
     * 格式化日期时间
     */
    function formatDateTime(date) {
        const y = date.getFullYear();
        const m = String(date.getMonth() + 1).padStart(2, '0');
        const d = String(date.getDate()).padStart(2, '0');
        const h = String(date.getHours()).padStart(2, '0');
        const min = String(date.getMinutes()).padStart(2, '0');
        const dayName = DAY_NAMES[date.getDay()];
        return `${y}-${m}-${d} ${h}:${min} (${dayName})`;
    }

    // ========== SQL 格式化 ==========

    const SQL_KEYWORDS = [
        'SELECT', 'FROM', 'WHERE', 'AND', 'OR', 'NOT', 'IN', 'LIKE', 'BETWEEN',
        'JOIN', 'LEFT', 'RIGHT', 'INNER', 'OUTER', 'FULL', 'CROSS', 'ON',
        'INSERT', 'INTO', 'VALUES', 'UPDATE', 'SET', 'DELETE',
        'CREATE', 'ALTER', 'DROP', 'TABLE', 'INDEX', 'VIEW', 'DATABASE',
        'PRIMARY', 'KEY', 'FOREIGN', 'REFERENCES', 'CONSTRAINT', 'UNIQUE',
        'ORDER', 'BY', 'GROUP', 'HAVING', 'LIMIT', 'OFFSET',
        'UNION', 'ALL', 'DISTINCT', 'AS', 'NULL', 'IS', 'EXISTS',
        'CASE', 'WHEN', 'THEN', 'ELSE', 'END',
        'COUNT', 'SUM', 'AVG', 'MIN', 'MAX',
        'ASC', 'DESC', 'WITH', 'RECURSIVE'
    ];

    const SQL_MAJOR_KEYWORDS = ['SELECT', 'FROM', 'WHERE', 'JOIN', 'LEFT JOIN', 'RIGHT JOIN',
        'INNER JOIN', 'OUTER JOIN', 'ORDER BY', 'GROUP BY', 'HAVING', 'LIMIT',
        'INSERT INTO', 'UPDATE', 'DELETE FROM', 'SET', 'VALUES', 'UNION', 'WITH'];

    /**
     * 格式化 SQL
     */
    function formatSQL(sql, options = {}) {
        if (!sql || typeof sql !== 'string') {
            return { error: '无效的 SQL 输入', result: '' };
        }

        const indent = options.indent || '  ';
        const uppercase = options.uppercase !== false;

        try {
            let result = sql.trim();

            // 规范化空白
            result = result.replace(/\s+/g, ' ');

            // 关键字大写
            if (uppercase) {
                SQL_KEYWORDS.forEach(keyword => {
                    const regex = new RegExp(`\\b${keyword}\\b`, 'gi');
                    result = result.replace(regex, keyword);
                });
            }

            // 主要关键字前换行
            SQL_MAJOR_KEYWORDS.forEach(keyword => {
                const regex = new RegExp(`\\s+${keyword.replace(' ', '\\s+')}\\b`, 'gi');
                result = result.replace(regex, '\n' + keyword);
            });

            // SELECT 后的字段
            result = result.replace(/SELECT\s+/i, 'SELECT\n' + indent);
            result = result.replace(/,\s*(?=[^\(]*(?:\(|$))/g, ',\n' + indent);

            // AND/OR 换行
            result = result.replace(/\s+(AND|OR)\s+/gi, '\n' + indent + '$1 ');

            // 括号内不换行（简化处理）
            // 处理逗号
            result = result.replace(/,\s*\n\s*(\w+\s*\()/g, ', $1');

            // 清理多余空行
            result = result.replace(/\n{3,}/g, '\n\n');
            result = result.trim();

            return { result: result, error: null };
        } catch (e) {
            return { error: e.message, result: sql };
        }
    }

    /**
     * 压缩 SQL
     */
    function minifySQL(sql) {
        if (!sql || typeof sql !== 'string') {
            return { error: '无效的 SQL 输入', result: '' };
        }

        try {
            let result = sql.trim();
            // 保留字符串内的空格
            const strings = [];
            result = result.replace(/'[^']*'/g, (match) => {
                strings.push(match);
                return `__STR_${strings.length - 1}__`;
            });

            // 压缩空白
            result = result.replace(/\s+/g, ' ');
            result = result.replace(/\s*([,()])\s*/g, '$1');
            result = result.replace(/\s*([=<>!]+)\s*/g, ' $1 ');

            // 恢复字符串
            strings.forEach((str, i) => {
                result = result.replace(`__STR_${i}__`, str);
            });

            return { result: result.trim(), error: null };
        } catch (e) {
            return { error: e.message, result: sql };
        }
    }

    /**
     * 提取 SQL 表名（简化版）
     */
    function extractTables(sql) {
        if (!sql) return [];
        const tables = new Set();

        // FROM 子句
        const fromMatches = sql.match(/\bFROM\s+([`"\[]?\w+[`"\]]?)/gi) || [];
        fromMatches.forEach(m => {
            const name = m.replace(/^FROM\s+/i, '').replace(/[`"\[\]]/g, '');
            tables.add(name);
        });

        // JOIN 子句
        const joinMatches = sql.match(/\bJOIN\s+([`"\[]?\w+[`"\]]?)/gi) || [];
        joinMatches.forEach(m => {
            const name = m.replace(/^JOIN\s+/i, '').replace(/[`"\[\]]/g, '');
            tables.add(name);
        });

        // INSERT INTO
        const insertMatches = sql.match(/\bINSERT\s+INTO\s+([`"\[]?\w+[`"\]]?)/gi) || [];
        insertMatches.forEach(m => {
            const name = m.replace(/^INSERT\s+INTO\s+/i, '').replace(/[`"\[\]]/g, '');
            tables.add(name);
        });

        // UPDATE
        const updateMatches = sql.match(/\bUPDATE\s+([`"\[]?\w+[`"\]]?)/gi) || [];
        updateMatches.forEach(m => {
            const name = m.replace(/^UPDATE\s+/i, '').replace(/[`"\[\]]/g, '');
            tables.add(name);
        });

        return Array.from(tables);
    }

    return {
        // IP 工具
        isValidIPv4,
        isValidIPv6,
        ipv4ToDecimal,
        decimalToIPv4,
        ipv4ToHex,
        ipv4ToBinary,
        parseCIDR,
        getIPClass,
        isPrivateIP,
        // Cron 工具
        parseCron,
        // SQL 工具
        formatSQL,
        minifySQL,
        extractTables
    };
});
