# Cadodile Trivia Quest

A touchscreen math trivia game built with Python and Kivy for the Raspberry Pi Zero 2 W. Designed to help 5th graders practice California Common Core math standards through a fun, retro pixel-art game experience.

---

## How It Works

When the game launches, players are greeted by a pixel-art start screen with three options: Singleplayer, Multiplayer, or Settings.

**Singleplayer** sends the player straight to the chapter select screen. **Multiplayer** first asks how many players are playing (2–4), then moves to chapter select. **Settings** lets you toggle stub mode for testing without hardware, adjust screen brightness, and test the block dispenser.

The chapter select screen lets players choose which math topic to practice. The five chapters cover the full Grade 5 CA Common Core math curriculum:

- **5.OA** — Operations and Algebraic Thinking (expressions, prime factors, patterns)
- **5.NBT** — Number and Operations in Base Ten (place value, decimals, multi-digit operations)
- **5.NF** — Number and Operations with Fractions (add, subtract, multiply, divide fractions)
- **5.MD** — Measurement and Data (unit conversions, volume)
- **5.G** — Geometry (coordinate plane, shape classification)

There is also an "All Chapters" option that mixes questions from every topic. Once a chapter is selected, the game begins.

Every question is generated with random numbers on the fly, so no two games are the same and students cannot memorize answers. The question generator creates fresh values for each problem while keeping the math difficulty appropriate for 5th grade. Questions are either multiple choice (4 options) or true/false.

During gameplay, the screen shows the current question, the player's score, and which player's turn it is in multiplayer mode. The player taps one of the answer buttons to respond.

If the answer is **correct**, the player earns a point (displayed as a "coin"), the servo motor activates to dispense a physical block as a reward, and the LED blinks for visual feedback. If the answer is **wrong**, the correct answer is displayed on screen. After a 2-second pause, the game moves to the next question. In multiplayer, turns rotate between players automatically.

After all 10 questions are answered (configurable in config.py), the game shows the end screen with final scores. In multiplayer, the winner is announced. Players can then choose to play again with new randomized questions, pick a different chapter, or return to the start screen.

The entire game runs without blocking the UI thread. All timed events use Kivy's Clock scheduler and all hardware actions run in background threads, keeping the touchscreen responsive at all times.

If the game is running on a computer without a Raspberry Pi, it automatically enters stub mode where all hardware actions (servo, LED) are printed to the console instead. This makes it easy to develop and test the game on any machine.

---

## Team

- [Name]
- [Name]
- [Name]
- [Name]
