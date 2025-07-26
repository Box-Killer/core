import { VNode } from "@vue/runtime-core";

declare global {
  namespace JSX {
    interface Element extends VNode {} // 将 JSX.Element 映射到 Vue 的 VNode
    interface IntrinsicElements {
      [key: string]: any;
    }
  }
}
