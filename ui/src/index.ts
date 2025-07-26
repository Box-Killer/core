import { defineComponent, toValue, watchEffect } from "vue";
import * as components from "./components";
import { useStyleTag } from "@vueuse/core";

export { components };

export function createVueComponent(name: string, props: any) {
  const component = components[name as keyof typeof components];
  if (!component) {
    throw new Error(`Component ${name} not found`);
  }
  return defineComponent({
    setup(_props, { emit }) {
      useStyleTag(component.styles);
      const renderer = component.setup(props, (result) => {
        const r = Object.fromEntries(
          Object.entries(result).map(([key, value]) => [key, toValue(value)])
        );
        emit("complete", r);
      });
      return renderer;
    },
  });
}

export function resultToText(result: any) {
  return Object.entries(result)
    .map(([key, value]) => `- ${key}: ${value}`)
    .join("\n");
}
