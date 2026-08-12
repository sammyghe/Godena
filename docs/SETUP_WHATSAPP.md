# Go live on WhatsApp — free, without owning a phone number

Meta gives you a **free test business phone number** the moment you create a WhatsApp app. You don't buy a number, you don't verify a business, and you don't need a SIM. ~10 minutes, all clicks, no code.

Godena is **reply-only** — it never messages anyone first. That means no message templates, no approval process, and replies land in WhatsApp's free service window.

---

## 1. Create the app (5 min)

1. Go to **[developers.facebook.com](https://developers.facebook.com)** → log in with your Facebook account → **My Apps** → **Create App**.
2. App type: **Business**. Name it `Godena`.
3. When asked for a Business Account, choose **create a test business account** — you do *not* need a verified business.
4. In the app dashboard, find **WhatsApp** in the product list → **Set up**.

A **test phone number** is created for you automatically. This is the number Godena will answer from.

## 2. Collect two values

On the WhatsApp → **API Setup** page:

- **Phone number ID** — a long number under the test number. Copy it. → this is `WHATSAPP_PHONE_ID`
- **Temporary access token** — click generate, copy it. → this is `WHATSAPP_TOKEN`

> The temporary token expires in 24 hours — fine for testing. For a permanent one: **Business Settings → System Users → Add** → assign the app → **Generate token** with the `whatsapp_business_messaging` permission. That token doesn't expire.

## 3. Add your test recipients

Still on **API Setup**, under "To": add up to **5 phone numbers** that are allowed to message the bot (your own WhatsApp, Amanuel's, a couple of testers). Each gets a confirmation code once.

Messages to and from these 5 numbers are **free and unlimited**.

## 4. Set the secrets on the Space

Go to **[the Godena Space settings](https://huggingface.co/spaces/sammygh/godena/settings)** → *Variables and secrets* → **New secret**, twice:

| Name | Value |
|---|---|
| `WHATSAPP_TOKEN` | the token from step 2 |
| `WHATSAPP_PHONE_ID` | the phone number ID from step 2 |

The Space restarts itself. Godena now prefers the official Cloud API automatically.

## 5. Point Meta at Godena

Back in the app: **WhatsApp → Configuration → Webhook → Edit**

| Field | Value |
|---|---|
| Callback URL | `https://sammygh-godena.hf.space/webhook` |
| Verify token | `godena` |

Click **Verify and save** (Godena answers Meta's handshake automatically), then **Manage** → subscribe to the **`messages`** field.

## 6. Test it

From one of your 5 verified numbers, WhatsApp the test number:

```
lawyer kampala
```

You should get three ranked results with real links. Try `ai video`, `pharmacy nairobi`, and `3` (share card).

---

## Going beyond 5 people

The test number is capped at 5 recipients. To open it up: add a **real phone number** (one that can receive an SMS/call and is not already on WhatsApp) in **API Setup → Add phone number**, then complete **Business Verification** in Business Settings (upload documents, 2–10 business days). After that you can message anyone, starting at 250 conversations/24h and scaling with quality.

**Timing note:** replies inside the 24-hour service window are free today, but Meta has announced that **from October 1, 2026** service messages become chargeable. Per-message costs are small, but plan for them — and never build the business model on the free tier.

## If something doesn't work

- **Webhook won't verify** → the Space must be awake (open `/health` first) and the verify token must be exactly `godena`.
- **No reply** → check the Space logs; confirm you subscribed to the `messages` field, and that your number is in the 5 allowed recipients.
- **"Token expired"** → generate a permanent System User token (step 2 note).
