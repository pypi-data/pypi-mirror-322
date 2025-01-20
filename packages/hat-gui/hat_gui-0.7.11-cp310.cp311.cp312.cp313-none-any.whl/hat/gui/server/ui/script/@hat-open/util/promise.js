/**
 * Create promise that resolves in `t` milliseconds
 */
export function sleep(t) {
    return new Promise(resolve => {
        setTimeout(() => { resolve(); }, t);
    });
}
/**
 * Delay function call `fn(...args)` for `t` milliseconds
 */
export function delay(fn, t = 0, ...args) {
    return new Promise(resolve => {
        setTimeout(() => { resolve(fn(...args)); }, t);
    });
}
/**
 * Create new future instance
 */
export function createFuture() {
    const data = {
        done: false,
        error: false,
        result: undefined,
        resolve: null,
        reject: null
    };
    const future = new Promise((resolve, reject) => {
        data.resolve = resolve;
        data.reject = reject;
        if (data.error) {
            reject(data.result);
        }
        else if (data.done) {
            resolve(data.result);
        }
    });
    future.done = () => data.done;
    future.result = () => {
        if (!data.done)
            throw new Error('future is not done');
        if (data.error)
            throw data.result;
        return data.result;
    };
    future.setResult = result => {
        if (data.done)
            throw new Error('result already set');
        data.result = result;
        data.done = true;
        if (data.resolve)
            data.resolve(data.result);
    };
    future.setError = error => {
        if (data.done)
            throw new Error('result already set');
        data.error = true;
        data.result = error;
        data.done = true;
        if (data.reject)
            data.reject(error);
    };
    return future;
}
