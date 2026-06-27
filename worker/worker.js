// Cloudflare Worker — Telegram webhook front-door.
// ACKs Telegram instantly (HTTP 200), verifies the secret-token header, then
// forwards the update to the FastAPI backend without blocking the response.
//
// Secrets/vars (set via `wrangler secret put` / wrangler.toml [vars]):
//   TELEGRAM_SECRET_TOKEN  — must match the backend's TELEGRAM_SECRET_TOKEN
//   BACKEND_URL            — e.g. https://api.codementor.example.com

export default {
  async fetch(request, env, ctx) {
    if (request.method !== "POST") {
      return new Response("ok", { status: 200 });
    }

    const secret = request.headers.get("X-Telegram-Bot-Api-Secret-Token") || "";
    if (secret !== env.TELEGRAM_SECRET_TOKEN) {
      return new Response("forbidden", { status: 403 });
    }

    const body = await request.text();

    // Fire-and-forget: forward to the backend, but ACK Telegram immediately.
    ctx.waitUntil(
      fetch(env.BACKEND_URL.replace(/\/$/, "") + "/webhook/telegram", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-Telegram-Bot-Api-Secret-Token": secret,
        },
        body,
      }).catch((e) => console.log("forward error:", e)),
    );

    return new Response(JSON.stringify({ ok: true }), {
      status: 200,
      headers: { "Content-Type": "application/json" },
    });
  },
};
