# "I Read Lev Goukassian's 'Mandated Ternary: Hardware Implementation of Ternary Logic' So You Don't Have To"

*Or: how one document about oxygen vacancies, memristors, and three states of matter
nearly destroyed my marriage and my career in the architecture team*

---

I read Lev Goukassian's "Mandated Ternary: Hardware Implementation of Ternary Logic" so you don't have to.

And no, I don't want your gratitude. I want you to understand the depth of my suffering. Last night at 2am I was weeping over a TaOx versus HfOx comparison table because I had run out of coffee and my wife had gone to bed with the words "you chose this life." She was right. I chose it. I clicked on a PDF with the confident title "Phase 1 - Device Physics, Circuit Primitives, and Physical Interlock Mechanisms," and the blue abyss of technical greatness opened beneath my feet.

The document reached me the standard way things reach people in 2026: someone dropped a link in the Telegram channel "Embedded Hardware Nerds," with the comment "guys, you have to see this circus." I was expecting another Arduino meme. I got 200 pages on how to make atoms obey three states of existence so that some nuclear reactor doesn't explode while the main log file is still waiting for its PUF signature.

You know that feeling when you're reading a solid-state physics dissertation and simultaneously understanding that the author is an absolute genius and an absolute madman in equal measure? Around page five, where Lev explains that Epistemic Hold is not "uncertainty" but "an authorized pause embedded in the crystal lattice of tantalum oxide," I understood that the ordinary world was over.

We live in a world where binary logic rules. Zero and one. False and true. Coffee or tea. Your wife says "it's fine" - which means in three hours you're sleeping on the couch. The binary world is understandable, predictable, and boring.

And Lev Goukassian proposes to wire a third option into matter itself.

"Abstain." Not as a software flag you can overwrite with a privilege escalation exploit. As a physical state of a resistor that survives a power cut. You can pull the plug, fly to a two-week vacation, come back, boot the server - and it will still be in the state of "I'm waiting for log confirmation, buddy. Don't touch anything."

When I grasped this, my fingers started itching. I immediately called Kevin, our lead embedded systems engineer. Kevin is famous for being able to write FPGA firmware on a restaurant napkin, but also for believing that "smart homes are a satanic invention."

"Kevin," I said. "Did you know you can make an unbreakable hardware-level lock at the transistor level? One that no software can bypass?"

"That's called a relay," Kevin answered sleepily (it was 2:15am). "Or pulling a fuse. Why are you awake?"

"I'm talking about three-valued logic, Kevin. There's a state called 'waiting for the log.' It survives power loss. You can't reset it by flashing new firmware."

"Are you on something?" Kevin asked, with genuine concern. "Or did you read that document?"

"Yes," I admitted. "Goukassian. Mandated Ternary."

"Oh," he said. "The one with 'No Log = No Action'? Where did you find it?"

"Someone posted it in Embedded Hardware Nerds."

"Ah. That's a trap. You're going to spend the next week with that look in your eyes, trying to integrate a memristive PUF into our Arduino side project, and then you'll quit to join a quantum mining startup. I've seen this ten times."

He hung up. I was left alone with the document, a cup of cold coffee, and the realization that somewhere in the world there is a person who seriously proposed using oxygen vacancy effects in binary tantalum oxide so that a chip can say "NO" with such force that it echoes across the next galaxy.

---

## How I Fell into the Three-State Rabbit Hole

You know what the scariest thing about Lev's document is? It opens with an epigraph. A self-quote, if I understood correctly:

*"Build the third state into matter, and the future stops pretending it never hesitated."*

I translated this for my wife at breakfast. She works in HR at a large tech company, so her reaction was predictable:

"We have a change approval policy at our company. If you build a third state into matter without sign-off from the architecture committee, you get fired. Also this sounds like something my ex would have said when trying to explain why we broke up. 'I was in a state of epistemic pause.'"

"It's different," I tried to explain. "The resistance switches between 1-10 kilohms, 100 kilohms to 1 megohm, and 1-10 megohms. It's physics."

"Honey," she took a bite of avocado toast, "I don't know what a kilohm is, but I know that last night you were talking in your sleep about IRS sigma/mu not exceeding 35 percent. And then you cried."

I didn't remember this. But I didn't rule it out.

The thing is, Lev writes like a god. He writes in a way that after five pages you start believing that the TaOx bilayer is not just a component but a character in a fantasy saga. It has two halves: TaOx+ (oxygen-rich, noble, fragile) and TaOx- (oxygen-depleted, dark, powerful). They battle. They create a filament - a conductive thread of oxygen vacancies. And then one of them breaks, and that gives you the intermediate resistance.

I pictured it as a battle between two armies. The Army of Oxygen Vacancies storms the TaOx+ barrier. Their general (let's call him Filament) shouts: "Forward, brothers! We must close the circuit and reach LRS - Proceed!" And behind them stands the stern log file whispering: "Easy, boys. The PUF signature isn't ready yet."

And when Lev writes about 20-year IRS retention - about how the intermediate state must survive two decades at 85 degrees Celsius without degradation - I suddenly understand that he is proposing to create an eternal soldier. A soldier standing guard at "Awaiting Authorization" who never dies. No battery. No reboot required. He simply exists. In silicon. In tantalum oxide. In my head now, permanently.

I made a note in the margin: "Lev - Terminator fan?"

Then I reached the NL=NA section - No Log = No Action.

This was the moment I stood up, walked around the room, sat back down, and read the paragraph three times.

Lev proposes a dedicated physical wire for the confirmation pulse. Not a data bus, not a software interrupt, not a flag in memory. A wire. Copper. On metal layer M3 or M4. Up to 500 micrometers long.

This wire connects to a window comparator that checks the voltage (1.5 to 2.5 volts) and pulse duration (20 to 80 nanoseconds). If the pulse doesn't meet spec - too short, too long, too weak, too strong - the comparator does not authorize the write to LRS (Proceed). Worse, it logs a TAMPER_EVENT_LOG and transitions the entire system to HRS (Refuse). Permanently.

This is like your front door lock requiring the key to have not only the right shape but also the exact weight, temperature, and smell. And if someone tries to pick it, the door doesn't just stay locked - it shouts "CAUGHT YOU" and pours concrete into the frame.

"This is madness," I said out loud. To an empty room. Because my wife had left for work.

I picked up my phone and wrote in the group chat "Developer Suffering Support":

"Guys, has anyone heard of Mandated Ternary? Is it normal that they propose detecting pulse forgery by measuring the rise time of the signal edge? Their tolerance is 20 to 50 picoseconds."

The responses:

- "Bro, you've lost it. Go to sleep."
- "20 picoseconds is less than the time light takes to cross a chip. Are you serious?"
- "Is Lev Goukassian a pseudonym? Maybe it's an AI?"
- "I work at TSMC. We don't have clients like this. And if we did, we'd send them to the department for psychotic states."

That last message calmed me a little. TSMC doesn't know about this, I thought - so it must all be theoretical fiction. But then I opened Section 12, the Bibliography.

Twenty sources. IEDM, APL, Nature Nanotechnology, Springer, Renesas MRAM datasheets, IRDS 2023-2024. All real. All peer-reviewed. All published in leading semiconductor journals and top conferences.

And one of the sources: TSMC Research, ISSCC 2024. 22nm 16-megabit ReRAM compute-in-memory macro.

TSMC knows. They just don't talk about it. Or they talk, but not to us.

I felt like the protagonist of a conspiracy thriller. Somewhere in a cleanroom in Taiwan, engineers in bunny suits are growing binary tantalum oxides with oxygen asymmetry, and in a parallel office Lev Goukassian is signing his documents ORCID: 0009-0006-5966-1243 and laughing at our binary souls.

---

## The Video Call with the Man Who Broke My Brain

Do you know what a "Voluntary Declaration of Continuity" is? I didn't either, until I finished the document.

Lev, it turns out, had notarized, time-stamped, and anchored in a blockchain (I am not joking, it says so in the document) a statement declaring that he refuses the role of "the only person who understands the whole system." The Bus Factor - the nightmare of every open source project - had been eliminated. No one can ever own or control Ternary Logic. No vendor. No corporation. Not even Lev himself.

This is so beautiful and so insane simultaneously that I couldn't hold back.

At the bottom of the document was a contact. Not a corporate email, not a feedback form. A personal Telegram handle.

I sat and stared at the screen for five minutes. Then I wrote:

"Lev, hello. I read your document on Mandated Ternary. Can I ask a couple of questions?"

The reply came in two minutes:

"Of course. Fair warning though - if you ask 'why not four states,' I will answer 'read Section 5.1' and hang up."

I almost laughed out loud. I wrote:

"No, I'm asking about the declaration. And about 20-year IRS retention. Is that real?"

"More real than your fear of deadlines," Lev replied. "We can call in half an hour. I'm doing verification on a test batch of PUFs right now - 1,000 dies - but it's boring. Call me."

Half an hour later I was sitting at the kitchen table, my wife not yet home, and I pressed "Video Call."

On the screen appeared a man of about fifty with salt-and-pepper in his beard, thick-framed glasses, and a t-shirt reading "I love Oxygen Vacancies." In the background I could see a rack of oscilloscopes and a cat bed where a ginger cat was sleeping.

"Lev Goukassian," he said. "You're the one who was crying in his sleep about sigma/mu?"

I went red. How did he know?

"Kevin messaged me. Said a friend was in trouble. Don't worry, it's normal. About 80% of first-time readers of the early document have nightmares about interconnects. By the fourteenth version you get used to it."

"You published fourteen versions?" I asked.

"Fourteen. Version thirteen had an error in the drift-diffusion equation for oxygen vacancies. Very embarrassing. But we fixed it."

I stared at him and couldn't believe it. This person - who is rewriting solid-state physics to build an ironclad prohibition system for critical infrastructure - is sitting in a t-shirt about vacancies with a cat.

"Lev," I said. "The main question. Do you genuinely believe this will work for 20 years at 85 degrees? Without IRS degradation?"

He sighed. Petted the cat.

"Listen," he said. "I'll tell you a secret. In our lab we have TaOx samples that have been sitting in a thermal chamber at 85 degrees since 2018. Seven years. IRS retention has dropped 12 percent. Arrhenius extrapolation gives a 95 percent lower confidence bound of 23 years at Ea equals 1.05 eV. That's almost 20 years. With margin. But I can't write that in the document because the IEDM reviewers will eat me alive for 'insufficient statistical significance.' So I wrote 'conditional pass' and passed the responsibility to Phase 2. Let the next generation suffer."

"And the PUF?" I asked. "Memristive PUF with 49% inter-die Hamming distance. Isn't that too low?"

Lev smiled. He pulled a board from under the table covered in a grid of chips.

"Here," he held it up to the camera. "512 dies. Measured inter-die HD - 50.2 percent. Look, here's the graph. Normal distribution. And the foundry signs the public key, not the private one. We designed it so that even if TSMC wanted to deceive us, they couldn't forge the signature. Because the private key is born after the foundry step, right on the die itself, from the quantum fluctuations of the filament."

He said this as casually as if he were explaining how to brew green tea.

"But the most important thing," he leaned closer to the camera. "Did you understand the declaration?"

"The Voluntary Declaration of Continuity?" I asked.

"Exactly. Bus Factor is when a project dies because the only developer gets hit by a bus. I don't want Ternary Logic to die with me. So I legally established that no single person, corporation, or government can control this system. It's embedded in matter. In tantalum oxide. In the rules of filament formation. Even if I'm gone, the chips will still say NO when they need to."

He fell silent. The cat meowed.

"What if someone reflashes the firmware?" I asked.

"Can't," Lev said flatly. "OTP fuses burn once. The mandate is written into the crystal. You can't change it remotely. Want to change the rules - make a new chip. That's a feature, not a bug."

I sat there absorbing the fact that this man had built a philosophy of refusal at the atomic level. Every chip with MT is a small anarchist that says "no" not because it was programmed to, but because its crystal lattice is built that way.

"Lev," I said. "Thank you. I'll probably never design systems like this. I'm just a developer."

"Developers matter too," he smiled. "Who's going to write the Epistemic Hold emulation on binary CMOS with a 1,400x energy penalty? Who's going to explain to the client why their server can't update its mandate over the air? That's all for developers. Go for it."

He waved, the cat jumped off the bed, and the call ended.

---

## An Epilogue That Could Have Been the End but Isn't

My wife came home from work and found me sitting at the kitchen table, laptop closed, staring into the middle distance.

"What's wrong?" she asked.

"I talked to Lev Goukassian," I said.

"The one who invented the third bit?"

"He didn't invent a bit. He invented a way to make silicon hesitate."

My wife sighed, put down her bag, and poured me some tea.

"You know," she said, "we have a rule in HR: if an employee quotes technical documentation in everyday conversation for three days running, we send them on paid leave. I'll file the paperwork tomorrow. Go to a museum. Or just sleep."

I nodded. But I knew I wouldn't sleep. Because now I saw the world differently. Every time my laptop froze with "waiting for server response," I understood - that's not a bug. That's Epistemic Hold. The server is waiting for confirmation from the log. It just doesn't have a confirmation pulse on a dedicated copper wire.

But one day it will.

And on that day the future will stop pretending it never hesitated.

And Lev Goukassian will be sitting in his lab, petting his cat, watching an oscilloscope, knowing that somewhere in the world a thousand chips are saying NO with absolute, physical, unrevokable certainty.

And that, damn it, is beautiful.

*End (or only the beginning, if you proceed to Phase 2)*
```
