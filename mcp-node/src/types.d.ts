declare module 'webview' {
  interface WebviewOptions {
    title?: string;
    width?: number;
    height?: number;
    dir?: string;
    [key: string]: any;
  }

  interface WebviewSpawnOptions extends WebviewOptions {
    cwd?: string;
    [key: string]: any;
  }

  interface Webview {
    binaryPath: string;
    optionsToArgv: (options: WebviewOptions) => string[];
    spawn: (options: WebviewSpawnOptions) => any;
  }

  const webview: Webview;
  export default webview;
} 