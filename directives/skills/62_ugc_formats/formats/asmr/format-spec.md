# Format spec, ASMR and Satisfying Demo

```
format_id:          ugc-asmr
command:            /pm-ugc-asmr
one_line:           The product's own sounds and textures carry the whole ad.

duration_s:         15 to 25            # measured median 19.2
script_default:     forbidden           # 0 of 10 banked ads speak
audio_treatment:    sound-led
delivery:           none
on_camera_share:    0%                  # hands only, no speaking face in any banked ad
rig:                static              # 10 of 10 banked ads
shots_per_10s:      6.5 to 8.0          # measured median (a FLOOR) to p75 (the target)

anchor_role:        product, sensory
requires:           product photo, a photo of every sensory state the ad shows
funnel_role:        awareness
authenticity:       high
generation_honesty: unconstrained
```

No `wps`, `word_budget`, `words_per_sentence` or `voice_source`: this format has no script.

## What this format is

The product's materials, motions and sounds are the entire ad. It removes the doubt "what is
this actually like to touch and hear", and it asks you to trust your own senses rather than
anyone's word. Nobody speaks, nobody is introduced, and there is no argument.

It is the only format in the family with no script, and narration would disqualify it: the
moment a voice explains what you are hearing, the sound stops being the content and becomes a
soundtrack.

## When it fits, and when it does not

```
fits:  the product has real texture, sound or motion worth hearing at close range
not:   software, services, anything with no physical presence
       the ad needs to explain a mechanism  -> route to /pm-ugc-expert
       the ad needs to teach a use          -> route to /pm-ugc-tutorial
       the product is only ever held sealed -> route to /pm-ugc-unboxing
```

**Brand familiarity warning, given once.** Research found ASMR produces negative brand attitudes
specifically for brands the viewer does not already recognise, and mixed effects among people
who do not experience ASMR at all. Say this plainly to the user before building, once, and
continue if they want it. It is a real effect and a soft one; it is their call.

## Beat order

1. **Trigger.** The first crisp sound, with the product already in frame as its source.
2. **Escalation.** Sensory beats building, each a different texture or motion.
3. **Use.** The product doing the thing it actually does, at close range.
4. **Resolution.** The satisfying settle. The ad ends on the product, cleanly presented.

## Hard rules

1. The product is on screen as the source of every sound. A sound with no visible cause is a
   dubbed sound.
2. No narration, no whisper voiceover, no spoken words anywhere.
3. No music, ever. This is the audio law, and it is not a hardship here: the sound IS the ad.
4. Macro or close framing throughout. A wide shot has no sensory content.
5. Every sensory state shown has a real user photo behind it, per the run engine's photo audit.
   The inside of a jar the model has never seen is the classic failure.
6. No on-screen text. The render carries none, as with every format.

## Compliance flags

| Flag | Rule |
|---|---|
| Health | structure and function language only if any claim appears in the caption; the ad itself makes none |
| Proof | this format proves nothing and claims nothing. Any claim belongs in the post copy, not here |

## Failure modes

1. **The soundtrack ad.** Pretty footage with a sound bed laid over it. Cause: treating sound as
   accompaniment rather than as content.
2. **The invented interior.** The lid comes off and the model has guessed what is underneath.
   Cause: skipping the photo audit.
3. **Cutting too fast.** Sensory beats need to land. A cut every second reads as a trailer.
4. **The wide shot.** Framing pulls back and the texture disappears. Nothing is satisfying at
   arm's length.
5. **No resolution.** The ad stops rather than settles, and the viewer feels the edit.

## The CTA question, answered honestly

There is no spoken CTA in this format and no on-screen text in any render. The ad therefore ends
on the product presented cleanly, and the actual call to action lives in the caption the user
writes when they post it. Say this at handover rather than pretending the video asks for
anything.

## Provenance

- Duration, rig, on-camera share and the absence of any script: measured from the ten banked ads
  in this skill's own bank, 2026-08. All ten are wordless.
- Brand-familiarity effect: Cohen et al., "Sonic sensations", Journal of Retailing and Consumer
  Services 2024, 80:103900.
- Beat order: house craft, written for this release.
