# Phase 2: The Spreadsheet of Destiny

## Or how I explained 64x64 crossbar tiles to my boss, my wife, and a cat named Schrödinger

---

I read Lev Goukassian's "Mandated Ternary: Hardware Implementation of Ternary Logic, Phase 2" so you don't have to.

You'd think after Phase 1 I would have learned my lesson. You'd be wrong. When the notification pinged from my Telegram channel "Silicon Valley Trauma Support Group" with the message "Phase 2 just dropped, boys," I was in a meeting. A real meeting, with my actual boss, a man named Greg who believes that "agile methodology" means everyone stands up for fifteen minutes and then ignores everything that was said.

Greg was explaining our Q3 roadmap for the nth time when my phone vibrated. I glanced down. The preview text read: "Section 4: System Architectures — Architecture A: Native Ternary Crossbar Compute-in-Memory. Architecture B: Hybrid Memristive-CMOS with Ternary State Controller."

I made a sound. It was not a human sound. It was the sound of a man who had just seen God and realized God speaks in SPICE models.

"You okay there, Dmitry?" Greg asked.

"Fine," I said. "Just remembered something about oxygen vacancy migration in TaOx bilayer systems."

Greg stared at me. My colleague Elena, who sits two desks over and has the patience of a saint and the sarcasm of a wounded komodo dragon, mouthed: "Stop. Just stop."

I did not stop.

---

How Phase 2 Found Me

The document reached me the same way Phase 1 did: someone who hates me and wants me to suffer dropped a link in a group chat. This time it was Alexei, my former roommate who now designs FPGAs for a defense contractor and has a beard that makes him look like a Tolstoy character who gave up on humanity.

"You're still alive?" he wrote. "Phase 2 is out. Lev went full economist. There's a spreadsheet."

"A spreadsheet?" I replied.

"With numbers, Dmitry. Break-even analysis. Market segmentation. He calculated the addressable market for financial settlement finality engines."

I felt a chill. Phase 1 was poetry. Phase 1 was about building the third state into matter, about making silicon hesitate, about oxygen vacancies marching like soldiers to form filaments of destiny. Phase 2, apparently, was about unit economics.

I opened the PDF on my phone. Greg was still talking about sprint planning. I scrolled.

Section 7.5: Addressable Market Quantification.

Table: Financial Settlement Finality Engines — approximately 70 central bank RTGS systems globally. Each requires approximately 10-50 MT enforcement chips. Total chips: approximately 6,600.

Unit selling price: $20,000 per chip.

Gross margin: $19,000 per chip.

Break-even volume: 947 units in year one.

I whispered, "He turned it into a business."

Elena leaned over. "What did you say?"

"Lev Goukassian," I said, "is selling chips for twenty thousand dollars each."

"And you're surprised?" she asked. "The man built a physical interlock that detects wire tapping by measuring pulse rise time in picoseconds. What did you think he was going to do, give it away on GitHub?"

She had a point.

---

The Call with Alexei (Former Roommate, Current Enabler)

I left the meeting early — Greg gave me a look that said "this will be in your performance review" — and called Alexei.

"Phase 2," I said. "Explain it to me like I'm five."

"You're never going to believe this," Alexei said. I could hear keyboard clacking in the background. He was probably simulating something. Alexei simulates things for fun. "Phase 1 was about whether you can make the third state exist in matter. Phase 2 is about whether you can sell it."

"That's not how science works."

"That's how survival works, Dmitry. Lev figured out that no foundry will build his PDK for the love of ternary logic. TSMC isn't a charity. They want to see a market."

I sat down on a bench outside the office. It was cold. San Francisco in November is not California; it's a conspiracy.

"What's the verdict?" I asked.

Alexei paused. "He has two architectures. Architecture A is the pure ternary crossbar. Beautiful. Elegant. Completely uneconomical for 2027. He calls it 'technically correct, economically premature.'"

"That's Lev for 'don't hold your breath.'"

"Exactly. Architecture B is the hybrid. Binary CMOS for computation, memristive cells just for enforcement. Separate lanes. Confirmation pulse on dedicated wires. He says it's ready for commercial pilots by Q4 2027."

"And the catch?"

"The catch," Alexei said, "is that the whole thing breaks even at fifteen percent market capture. If they can't get that, the program needs a government mandate or a consortium of banks and grid operators to co-fund the NRE."

"NRE?"

"Non-recurring engineering. Thirteen million dollars, central estimate."

I did the math in my head. "That's... not that much?"

"For a niche product? It's huge. But for the people who lose a billion dollars when a settlement engine fails? It's nothing. Lev's whole argument is that the people who need this really need it, and they have very deep pockets."

I thought about this. I thought about the financial settlement engine in Phase 2 — the one that holds funds in escrow until the log is signed, the one that can't be bypassed by any software exploit because the circuit breaker is physically gated by a memristor.

"Alexei," I said, "are we going to build this?"

"We?" He laughed. "Dmitry, we're two guys with laptops and questionable sleep schedules. We're not building anything. But someone will. And when they do, every high-frequency trading firm is going to want one."

"Why?"

"Because," Alexei said, "if you're moving a billion dollars and the system says 'hold' while it verifies the log, you want that hold to be physically real. You want it to survive a power outage. You want it to be provable in court twenty years later. Lev built that. Phase 2 proves it works."

---

The Spreadsheet That Changed Everything

I went home that night and read Phase 2 from beginning to end. All 14 sections. All 20+ pages of economics, certification timelines, and crossbar scaling limits.

Here's what I learned.

First: The 64x64 crossbar limit from Phase 1 is real. You can't put more than 4,096 memristor cells in a single block without IR drop ruining your sensing margins. But Lev figured out hierarchical tiling — stacking blocks like Legos, adding repeaters between them — and proved that wire energy is negligible. The binding constraint is voltage drop, not physics. It's an engineering problem, not a dealbreaker.

Second: The certification path exists. IEC 61508 SIL 3 by Q4 2027. That's the functional safety standard for nuclear plants and aircraft. Lev's team (or whoever he's working with — the document is coy about organizational details) plans to submit their evidence package to TÜV SÜD or exida by Q2 2027.

I texted Elena: "Do you know what TÜV SÜD is?"

She replied: "German certification body. If they say your chip is safe, banks buy it. If they don't, you sell it to hobbyists on Tindie."

Third: The economics are weird. Lev's numbers say that at $20,000 per chip and 6,700 chips per year, the total addressable market is $135 million annually. That's real money. But it's not smartphone money. It's not AI accelerator money. It's infrastructure money — boring, steady, and completely dependent on regulatory momentum.

"If the SEC doesn't mandate hardware-enforced audit trails," Lev writes somewhere in Section 12, "MT remains optional. If they do, MT becomes mandatory."

That's the whole bet. That's the whole thesis. Build the third state into matter, and wait for the regulators to notice that software can be hacked.

---

The Video Call with Lev (Part Two)

I couldn't help myself. I messaged Lev again.

"Phase 2. Spreadsheets. Really?"

His reply came in thirty seconds: "Economics is just physics with money. Want to call?"

Twenty minutes later we were on video. Same lab. Same cat. Same t-shirt, but this one said "I <3 IR Drop."

"Congratulations," I said. "You wrote a business plan."

Lev shrugged. "If the technology works but nobody builds it, the technology doesn't work. That's not cynicism. That's reality."

"You really think banks will pay twenty thousand dollars per chip?"

"They pay more for less," he said. "Have you seen what a hardware security module costs? And those don't have power-loss-persistent Epistemic Hold. They don't have NL=NA. They don't have PUF-rooted provenance from the foundry. MT gives you all three."

"But the certification — IEC 61508 — that's years of work."

Lev smiled. "That's why Phase 2 has a timeline. Q1 2026: test vehicle on N2 CMOS. Q2: IRS accelerated aging. Q3: NL=NA attack battery. Q4: IEC pre-assessment. Q1 2027: first functional chip. Q2: certification submission. Q3-Q4: commercial pilots."

"That's insane."

"That's planning, Dmitry. You should try it sometime."

The cat jumped onto the keyboard. Lev pushed it away gently. "The real question," he said, "is whether you want to be involved."

"Me?" I laughed. "I'm a software engineer. I write Python. I argue about indentation."

"And you read both phases of a hardware architecture document. You cried in your sleep about sigma/mu. You called me twice. You're not a software engineer, Dmitry. You're someone who hasn't admitted they want to build hardware."

I didn't have an answer to that.

---

The Argument with My Wife (Real Name: Natasha, Patience: Finite)

Natasha found me at 1 AM staring at Lev's crossbar diagrams.

"You're doing it again," she said.

"Doing what?"

"The thing where you forget that you have a job, a wife, and a functioning circulatory system because a man in a cat-themed t-shirt told you about oxygen vacancies."

I closed the laptop. "Phase 2 has a spreadsheet."

"I'm sure it does."

"It calculates the break-even volume for a memristive enforcement chip. Nine hundred forty-seven units in year one. At twenty thousand dollars each."

Natasha sat down. She's an HR director. She deals with people who think they're more important than they are. Dealing with me must be exhausting.

"Dmitry," she said, "are you going to quit your job and join this man's startup?"

"I don't think it's a startup. I think it's a movement."

"That's worse. Movements don't have health insurance."

I wanted to argue, but she was right. Lev's document doesn't mention a company name. It doesn't mention investors or employees or office locations. It mentions ORCID: 0009-0006-5966-1243 and a Voluntary Declaration of Continuity that prevents anyone from owning Ternary Logic.

"He's not building a company," I said slowly. "He's building a standard. He wants MT to be like TCP/IP — a protocol that everyone uses and no one owns."

Natasha sighed. "And you want to help him."

"I want to understand him."

"That's the same thing, Dmitry. That's always been the same thing."

She went to bed. I opened the laptop again.

---

The Two Architectures (As Explained to a Drunk Person at a Party)

Imagine you're at a party. Someone asks what you do. You say "hardware enforcement of ternary logic for autonomous settlement systems." They walk away. This has happened to me twice.

Here's how I now explain Phase 2:

Architecture A is like building a city where every street is designed for ternary logic. Beautiful. Efficient. Requires rebuilding everything from scratch. Nobody has that kind of money or patience.

Architecture B is like adding a ternary enforcement layer on top of an existing binary city. You keep the old streets. You add new bridges. It's uglier, but it works now, and you can certify it faster.

Lev recommends Architecture B for 2027. Architecture A is for 2030, when everyone has admitted that binary isn't enough.

"Binary isn't enough" is the part that scares people. Binary has been enough for seventy years. Binary built the internet. Binary landed rovers on Mars. Binary made TikTok recommend videos that rot your brain with algorithmic precision.

But binary can't say "I'm holding your billion dollars until I verify the log, and I will continue holding it through a power failure, and I will prove to a court in 2046 that I never let go."

Binary needs software for that. Software can be hacked. Software can be bypassed. Software can be lied to.

Matter cannot be lied to. That's Lev's whole argument. That's why he's willing to spend years of his life on oxygen vacancies and window comparators and PUF signatures.

---

The Cat Theory of Ternary Logic

Near the end of our call, I asked Lev about the cat.

"Schrödinger?" he said. "He's named after the physicist. But not for the reason you think."

"Go on."

"Everyone thinks Schrödinger's cat is about superposition. Alive and dead at the same time. That's not what the thought experiment was about. It was about measurement. About the fact that the cat's state is indeterminate until you open the box."

He petted the cat. The cat purred.

"Binary logic is like that. You don't know if a bit is 0 or 1 until you read it. But the read itself can disturb the state. Ternary is different. The third state — Epistemic Hold — is not indeterminate. It's determinately waiting. It's not that we don't know. It's that we're not allowed to proceed until something happens outside the system."

"The confirm pulse," I said.

"The confirm pulse. Exactly. The cat isn't alive and dead. The cat is sitting there, perfectly healthy, refusing to come out of the box until you say the magic word. That's Epistemic Hold. That's NL=NA. That's MT."

I looked at the cat. The cat looked at me. I could not tell if it was judging me or simply hungry.

"Schrödinger approves," Lev said. "He's been in the lab for six years. Never once has he accidentally transitioned from IRS to LRS without a confirm pulse."

"That's either very impressive or very concerning."

"Both," Lev said. "Both is good."

---

What I'm Going to Do About It

I haven't quit my job. Not yet. But I've started reading about memristors. I've started simulating crossbar arrays in my free time. I've started talking to Elena about whether our company might need MT enforcement for something — anything — so I can justify spending work hours on this.

Elena, who is smarter than me and knows it, said: "Dmitry, we build ad tech. We show people shoes they don't need. We don't need hardware-enforced Epistemic Hold."

"We might," I said weakly.

"We won't."

"Then I'll do it on my own time."

She looked at me with something that might have been pity or might have been respect. "You're really going to do this, aren't you? You're going to try to build ternary logic in your garage like it's 1976 and you're Steve Jobs."

"I'm not building anything. I'm just... learning."

"Learning is the first step to building."

I didn't argue.

---

The Bottom Line (Because Phase 2 Has One)

Lev's Phase 2 document ends with a conclusion: MT is physically realizable, architecturally viable, economically achievable with consortium co-investment, and certifiable to IEC 61508 SIL 3 by Q4 2027.

That's the good news.

The bad news is that none of this happens automatically. Someone has to build the test vehicle. Someone has to run the accelerated aging tests. Someone has to convince a foundry to add TaOx BEOL layers to their process. Someone has to raise the money.

That someone might be Lev. He seems to have a lab, a cat, and a bottomless well of determination. But even Lev can't do it alone.

"Phase 3," he said at the end of our call, "is about deployment. About writing the software stack that talks to the MT chips. About building the compilers and the audit tools and the regulatory frameworks."

"That sounds like a lot of work."

"It's twenty years of work, Dmitry. That's the point. The third state isn't a product. It's a foundation. It's the thing you build on top of for decades."

"And you want me to help."

"I want you to stop pretending you're just a spectator. You read both phases. You called me twice. You cried about sigma/mu. You're not a spectator. You're an early adopter who hasn't admitted it yet."

I hung up. I sat in the dark. The cat — my cat, not Schrödinger — jumped onto my lap. Her name is Masha. She has no opinion on ternary logic, but she appreciates consistent feeding schedules.

"Dmitry," Natasha called from the bedroom, "are you coming to bed?"

"Soon," I said.

I opened the laptop. I started a new document. I titled it "MT_Phase_3_Notes."

I have no idea what I'm doing. But I'm doing it anyway.

---

End of Phase 2 Story. Phase 3: Deployment, Madness, and the Regulatory Capture of Reality — coming soon to a Telegram channel near you.
