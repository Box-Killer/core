import { ref } from "vue";
import { defineComponent } from "../utils";
import * as z from "zod";

export default defineComponent(
  {
    name: "Choose",
    description: "Choose one of the options",
    schema: z.object({
      options: z.array(z.string()),
    }),
  },
  ({ options }, complete) => {
    const chosen = ref<number>();
    return () => (
      <div className="choose">
        {options.map((option, index) => (
          <div
            key={index}
            className={
              chosen.value === index ? "choose-card chosen" : "choose-card"
            }
            onClick={() => (chosen.value = index)}
          >
            <span
              className="choose-card-label"
              innerHTML={option}
            />
            {chosen.value === index && (
              <span className="choose-card-check">✓</span>
            )}
          </div>
        ))}
        <button
          disabled={chosen.value === undefined}
          className={
            chosen.value === undefined ? "geist-btn disabled" : "geist-btn"
          }
          onClick={() => {
            if (chosen.value !== undefined) {
              complete({
                chosen: String(chosen.value),
                name: options[chosen.value],
              });
            }
          }}
        >
          完成
        </button>
      </div>
    );
  },
  `
  .choose {
    display: flex;
    flex-direction: column;
    gap: 10px;
    align-items: center;
    padding: 12px 0;
    font-family: 'Geist', 'Inter', 'Helvetica Neue', Arial, sans-serif;
    background: #fff;
    border-radius: 8px;
    box-shadow: none;
    min-width: 220px;
    max-width: 320px;
    margin: 0 auto;
  }
  .choose-card {
    width: 100%;
    min-width: 140px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 8px 14px;
    border-radius: 6px;
    background: #fafbfc;
    box-shadow: none;
    border: 1px solid #ececec;
    font-size: 15px;
    color: #222;
    cursor: pointer;
    transition: border 0.15s, background 0.15s, color 0.15s;
    margin-bottom: 1px;
    position: relative;
  }
  .choose-card:hover {
    border: 1px solid #0070f3;
    background: #f5f7fb;
    color: #0070f3;
  }
  .choose-card.chosen {
    border: 1.5px solid #0070f3;
    background: #eaf4ff;
    color: #0070f3;
    font-weight: 600;
  }
  .choose-card-label {
    flex: 1;
    font-size: 15px;
    letter-spacing: 0.01em;
  }
  .choose-card-check {
    font-size: 15px;
    color: #0070f3;
    margin-left: 8px;
    font-weight: bold;
    user-select: none;
  }
  .geist-btn {
    margin-top: 10px;
    padding: 7px 18px;
    border-radius: 6px;
    background: #0070f3;
    color: #fff;
    font-size: 15px;
    font-weight: 500;
    border: none;
    cursor: pointer;
    box-shadow: none;
    transition: background 0.15s, color 0.15s, opacity 0.15s;
    letter-spacing: 0.01em;
  }
  .geist-btn:hover:not(.disabled) {
    background: #0051a3;
    color: #fff;
    opacity: 0.95;
  }
  .geist-btn.disabled {
    background: #ececec;
    color: #bdbdbd;
    cursor: not-allowed;
    opacity: 0.7;
    box-shadow: none;
  }
  `
);
