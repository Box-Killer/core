import { MaybeRefOrGetter } from "vue";
import * as z from "zod";

export interface Component<T> {
  options: {
    name: string;
    description: string;
    schema: z.ZodSchema<T>;
  };
  setup: (
    props: T,
    complete: (result: Record<string, MaybeRefOrGetter<null | string>>) => void
  ) => () => JSX.Element;
  styles: string;
}

export function defineComponent<T>(
  options: Component<T>["options"],
  setup: Component<T>["setup"],
  styles: string
): Component<T> {
  return {
    options,
    setup,
    styles,
  };
}
