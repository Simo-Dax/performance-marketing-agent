# UGC image engine, the anchor still

One job: produce the still that holds identity for the whole ad. This engine runs in TWO PHASES.

| Phase | When | Produces |
|---|---|---|
| **Phase 1, the anchor prompt** | after the shot count is set, BEFORE gate 1 | the written prompt, which rides into gate 1 beside the script |
| **Phase 2, the render** | at gate 2, after the user approves the plan | the actual image, which costs money |

I.1 to I.3 are phase 1 and are free. I.4 to I.5 are phase 2 and spend. Writing the prompt is
free, so it happens early and the user approves the IDEA of the anchor before paying for it.

The anchor locks whatever RECURS across the ad. What recurs is a fact about the FORMAT, stated
in its shot vocabulary and its `anchor_role`, not something that has to be derived from a shot
list: a testimonial recurs on one speaker, a street interview on the interviewer only, an
unboxing on hands and a container.

Most of what you need is not in this file. It is in the ten anchor prompts in this skill's own
`references/recreation-prompts/anchor/`. READ ALL TEN before writing anything, and never read
another format's bank. The rules below are only the things the bank cannot teach you.

---

## I.1 What the anchor is for, and how to choose it

The anchor is the reference the video call carries so the character and the product are the
same character and the same product at second 29 as at second 1.

**The anchor is chosen for legibility, not chronology.** It does NOT have to be the first
frame, or any frame the ad actually contains. Pick the moment where whatever must stay
constant is shown BEST: face clearest, product label most readable, both largest in frame.

The rule, simply:

> **Whatever has to stay the same for the whole ad has to be in the anchor.** If the ad shows
> a consistent character using a product, the anchor contains BOTH the character and the
> product, together, in one frame. If only the product persists, the anchor is the product. If
> only a person persists, the anchor is the person. Nothing that has to persist is left out,
> and nothing that does not persist is added.

The format spec names which of those applies. Follow it.

**A format may declare a PLATE SET rather than one still.** When its `anchor_role` says so, build
every plate the spec defines and note which shots each one carries. This is a different question
from the one-per-person rule below, which is about not building a still for every face.

**One anchor per ad, not one per person.** The anchor locks what RECURS. Anyone who appears once
and is never seen again does not need one, and the video model handles them inside the render.
A street interview is the clearest case: the interviewer is in most of the ad and gets the
anchor, while each respondent appears for a few seconds and is generated in the video. Do not
build a still for every face that will be on screen; build one for every face that has to still
be the same face later.

**The person is generated for this ad.** Unless the user has a saved character in
`11_Characters/`, in which case use it, the anchor invents the person from the casting brief in
the format spec, which is the brand's ideal customer from the VOC or the Foundation Pack avatar.
When a person is generated, offer once at the end to save them to the cast so the next ad can
reuse the same face.

## I.2 The fixed blocks, reused verbatim

Every one of the 110 anchor prompts in the banks carries the same technical preamble. It is
house boilerplate, not competitor creative, so it is REUSED VERBATIM and is the one part of a
bank file you may copy. Read them from your bank and carry them across unchanged:

1. The `ANCHOR FRAME RECREATION PROMPT` header and the photoreal register line.
2. The realism sentence: natural skin texture, real hair detail, believable hands and fingers,
   subtle lens softness, phone-camera dynamic range, ordinary consumer lighting.
3. The no-beautify ban: no fashion-model retouching, no cinematic haze, no studio product render.
4. The no-overlay ban: no subtitles, captions, stickers, watermarks, app UI or source-brand
   graphics, and the only readable branded text is what physically exists on the product.
5. The product-substitution contract: the user's uploaded product image is the ONLY product
   reference, it replaces the source product completely, and its silhouette, proportions, cap or
   lid, material finish, colors, logo, typography, label layout and every visible printed word
   survive unchanged. The hand poses around the real geometry; the product is never warped to
   fit the hand.
6. The `Critical fidelity:` closing block.

## I.3 The one part you write

`Composition and scene:` is the only variable block, and it is a single paragraph. It names the
person (or the hands), the wardrobe and accessories that must persist, the product and how it
is held or placed, the setting, the light, and the framing. Physical facts only. No mood words,
no brand adjectives, no art direction.

Write it fresh every time. It is the one block that must never echo a bank example.

Length: the banks run 1,837 to 2,668 characters end to end, mean 2,278. Land in that band.

## I.4 The call, phase 2

Nothing below runs until the user has approved the plan at gate 1.


| | |
|---|---|
| Model | GPT Image 2 where the format's spec says so, Nano Banana as the cheaper alternative |
| References | GPT Image 2 takes them on `input_urls`, Nano Banana on `image_urls`, never the other way |
| Aspect | `9:16`, set explicitly; `auto` silently downgrades a GPT Image 2 render to 1K |
| Resolution | `4K` on GPT Image 2 at this aspect |

The user's product photo is always a reference. A saved character adds a second. Upload each
once and reuse the URL.

While collecting these, also collect the product's IN-USE states if the ad will show the product
being opened, applied, poured, worn or demonstrated. The anchor itself rarely needs them, but the
video stage does, and asking once here is cheaper than stopping the run later to ask again.

## I.5 GATE 2, permission to spend on the anchor

Generating the anchor costs the user money. Ask before, never after. The prompt itself was
already approved at gate 1, so this gate asks one narrower question: spend on rendering it.

State in one line what will be generated and what it costs, then WAIT for an explicit yes. No
image is created on a maybe, on silence, or on an approval given for something else earlier in
the run.

Once it renders, show it and ask whether the person and the product are right. A wrong anchor is
corrected here, where a retry costs an image, and never later, where it costs a video.

Two stills maximum before asking for direction; a third attempt with no user note is guessing
with their money. Each retry is a fresh spend and needs its own yes.

## I.6 Self-check

- everything the format says must persist is in the frame, and nothing else is
- the product's printed text is legible and unaltered
- wardrobe and accessories that must persist are visible and named in the prompt
- the fixed blocks are present and unedited
- the composition paragraph is original, states physical facts, and carries no mood words
- 9:16, explicit aspect, no captions or watermarks anywhere in the image
- the prompt went to the user at gate 1 and the render happened only after gate 2
