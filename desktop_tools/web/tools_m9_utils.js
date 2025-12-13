/* 工具箱（M9）密码生成器算法
 *
 * 设计目标：
 * - 纯算法、无 DOM 依赖
 * - 使用 crypto.getRandomValues 保证安全随机
 */
(function (root, factory) {
    if (typeof module !== 'undefined' && module.exports) {
        module.exports = factory();
    } else {
        root.DogToolboxM9Utils = factory();
    }
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
    'use strict';

    // 字符集定义
    const CHAR_SETS = {
        uppercase: 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
        lowercase: 'abcdefghijklmnopqrstuvwxyz',
        numbers: '0123456789',
        symbols: '!@#$%^&*()_+-=[]{}|;:,.<>?'
    };

    // 相似字符（易混淆）
    const SIMILAR_CHARS = '0OoIl1';

    /**
     * 获取安全随机整数 [0, max)
     */
    function secureRandomInt(max) {
        if (max <= 0) return 0;
        if (typeof crypto !== 'undefined' && crypto.getRandomValues) {
            const array = new Uint32Array(1);
            crypto.getRandomValues(array);
            return array[0] % max;
        }
        // 兜底（不安全，仅用于无 crypto 环境）
        return Math.floor(Math.random() * max);
    }

    /**
     * Fisher-Yates 洗牌算法
     */
    function shuffle(array) {
        const arr = array.slice();
        for (let i = arr.length - 1; i > 0; i--) {
            const j = secureRandomInt(i + 1);
            [arr[i], arr[j]] = [arr[j], arr[i]];
        }
        return arr;
    }

    /**
     * 生成单个密码
     * @param {Object} options
     * @param {number} options.length - 密码长度 (8-128)
     * @param {boolean} options.uppercase - 包含大写字母
     * @param {boolean} options.lowercase - 包含小写字母
     * @param {boolean} options.numbers - 包含数字
     * @param {boolean} options.symbols - 包含特殊符号
     * @param {boolean} options.excludeSimilar - 排除相似字符
     * @returns {string}
     */
    function generatePassword(options) {
        const {
            length = 16,
            uppercase = true,
            lowercase = true,
            numbers = true,
            symbols = false,
            excludeSimilar = false
        } = options || {};

        // 构建字符池
        let charPool = '';
        const requiredChars = [];

        if (uppercase) {
            let chars = CHAR_SETS.uppercase;
            if (excludeSimilar) chars = removeSimilar(chars);
            charPool += chars;
            if (chars.length > 0) requiredChars.push(chars);
        }
        if (lowercase) {
            let chars = CHAR_SETS.lowercase;
            if (excludeSimilar) chars = removeSimilar(chars);
            charPool += chars;
            if (chars.length > 0) requiredChars.push(chars);
        }
        if (numbers) {
            let chars = CHAR_SETS.numbers;
            if (excludeSimilar) chars = removeSimilar(chars);
            charPool += chars;
            if (chars.length > 0) requiredChars.push(chars);
        }
        if (symbols) {
            let chars = CHAR_SETS.symbols;
            if (excludeSimilar) chars = removeSimilar(chars);
            charPool += chars;
            if (chars.length > 0) requiredChars.push(chars);
        }

        if (charPool.length === 0) {
            throw new Error('至少选择一种字符类型');
        }

        const pwdLength = Math.max(8, Math.min(128, length));

        // 确保每种字符类型至少出现一次
        const password = [];
        for (const chars of requiredChars) {
            if (password.length < pwdLength) {
                password.push(chars[secureRandomInt(chars.length)]);
            }
        }

        // 填充剩余位置
        while (password.length < pwdLength) {
            password.push(charPool[secureRandomInt(charPool.length)]);
        }

        // 打乱顺序
        return shuffle(password).join('');
    }

    /**
     * 批量生成密码
     * @param {Object} options - 同 generatePassword
     * @param {number} count - 生成数量 (1-100)
     * @returns {string[]}
     */
    function generatePasswords(options, count) {
        const n = Math.max(1, Math.min(100, count || 1));
        const results = [];
        for (let i = 0; i < n; i++) {
            results.push(generatePassword(options));
        }
        return results;
    }

    /**
     * 移除相似字符
     */
    function removeSimilar(str) {
        return str.split('').filter(c => !SIMILAR_CHARS.includes(c)).join('');
    }

    /**
     * 计算密码强度 (0-100)
     */
    function calculateStrength(password) {
        if (!password) return 0;

        let score = 0;
        const len = password.length;

        // 长度评分
        if (len >= 8) score += 10;
        if (len >= 12) score += 10;
        if (len >= 16) score += 10;
        if (len >= 20) score += 10;

        // 字符多样性
        if (/[a-z]/.test(password)) score += 15;
        if (/[A-Z]/.test(password)) score += 15;
        if (/[0-9]/.test(password)) score += 15;
        if (/[^a-zA-Z0-9]/.test(password)) score += 15;

        return Math.min(100, score);
    }

    /**
     * 获取强度标签
     */
    function getStrengthLabel(score) {
        if (score < 30) return { label: '弱', color: 'danger' };
        if (score < 60) return { label: '中等', color: 'warning' };
        if (score < 80) return { label: '强', color: 'success' };
        return { label: '非常强', color: 'success' };
    }

    return {
        generatePassword,
        generatePasswords,
        calculateStrength,
        getStrengthLabel,
        CHAR_SETS,
        SIMILAR_CHARS
    };
});
