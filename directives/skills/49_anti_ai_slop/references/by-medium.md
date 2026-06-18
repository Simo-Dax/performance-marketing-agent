# Rules By Medium

Same anti-slop core, different shape for each output type. Load the matching
section based on what's being rewritten.

## Landing pages

- **Hero headline**: max 8 words. One concrete promise. State what the user gets, not what the company "empowers". No abstract nouns (landscape, ecosystem, journey, experience).
- **Subheadline**: max 18 words. Who it's for + what changes after they use it. No "leveraging", no "seamlessly".
- **CTA buttons**: 2-4 words, verb-first, first-person where possible ("Get my audit" beats "Learn more"). Never "Click here", "Submit", "Get started" alone.
- **Section headers**: sentence case, one idea. No "Empowering X to do Y".
- **Feature blurbs**: name the feature, then one sentence in user-terms. No "powered by", no "AI-driven".
- **Social proof captions**: real names + numbers + outcomes. Never "trusted by industry leaders".
- **FAQ answers**: lead with the answer in the first 6 words. No "Great question!". No "It depends" without a real answer.
- **Pricing tier names**: concrete or branded, never default "Standard / Professional / Enterprise".
- **Empty states**: tell the user what to do next, not what's missing. "Add your first client" beats "No clients found".

## Cold emails

- **Subject line**: max 5 words. Lowercase. Looks like a real person sent it. No "Quick question", "Following up", "Touching base".
- **Opener**: not "I hope this email finds you well", not "I came across your profile". Reference one concrete thing.
- **One paragraph max for the pitch**. No three benefits. One ask.
- **Sign-off**: first name only. No "Best regards" + 4-line signature on the first touch.
- **No links in the first email** unless directly asked.
- **No "circle back" / "touch base" / "synergies" / "leverage"** ever.

## LinkedIn DMs

- **First message**: max 3 lines. No pitch. One concrete thing from their world.
- **Never start with "Hi [Name], hope you're doing well"**. Skip the throat-clear.
- **No "I'd love to connect" / "I'd love to learn more"**. Say why.
- **No questions ending in "?"** until message 2 or 3 unless it's specific to them.
- **One CTA per message, max**.

## LinkedIn posts

- **First line is the hook**. Not "Here's a thread on...". Show the surprise, the number, or the controversial take.
- **Short paragraphs (1-2 sentences each)**. Each line breaks.
- **No "P.S. follow me for more"**. No "Agree? Comment below". No "♻️ Repost if you found this valuable".
- **No three-emoji bullet lists** (✅ ✅ ✅). Use plain hyphens or numbers.
- **No "In today's X landscape"**. Ever.
- **Voice match required**: load `walid-writing-style.md` (or the relevant style file) before rewriting.

## Proposals

- **Section headers in sentence case**.
- **No "We are excited to partner with you"** boilerplate.
- **Each section answers one question the client asked or implied**. If you can't name the question, cut the section.
- **No "comprehensive solution" / "tailored approach" / "best-in-class"**. Show, don't tell.
- **Pricing tables: numbers, deliverables, dates. No prose around them.**
- **Next steps: a list of 3 max, each with an owner and a date.**

## Documentation / SOPs

- **Imperative voice for steps**: "Click X", not "You will click X" or "The user should click X".
- **One step per line**.
- **No "Now that we've covered X, let's move on to Y"**. Just move on.
- **No "Welcome to this guide on..."**. Title is enough.
- **Screenshots > paragraphs of description.**

## App microcopy

- **Buttons**: verb-first, 1-3 words.
- **Error messages**: what happened + what to do. Never just "An error occurred".
- **Confirmation dialogs**: state the consequence ("Delete 3 clients permanently"). Not "Are you sure?".
- **Tooltips**: one sentence max. No marketing.
- **Onboarding tooltips**: tell the user what to click, not why it's important.

## Voice-aware rewriting

If a `walid-writing-style.md`, `ayautomate-tone-of-voice.md`, or similar style
file is referenced in CLAUDE.md or the conversation, load it BEFORE rewriting.
The anti-slop rules are the floor; the style file is the ceiling. Don't strip
voice features (Walid's short sentences, direct hits, no fluff) while removing
AI tells.
