This repository contains an AI-assisted formalization in Lean 4 of the preprint "Asymptotically attaining the Moore bound" by W. Cames van Batenburg and S. Korsky, August 4, 2026, available at https://arxiv.org/abs/(TO BE INSERTED LATER).


Neither of the two authors is a native speaker of Lean. It is therefore conceivable that the formalization is not up to the standard of experienced Lean users. We welcome independent checks by humans. In normal times, such independent human expert checks would have been sought prior to submission to arXiv, but in the age of AI acceleration it seems more prudent to move fast. That being said, we have made the following precautions: 


We checked the formalization among 6 independent sessions of ChatGPT and Claude, asking it to "find the weaknesses" or "why is this formalization not complete?".  An example of a full prompt we used is:

"
Please consider the attached attempted formalization in Lean 4 of the attached preprint. Please identify the mistakes and then explain to me why this formalization is incorrect or incomplete. In particular, check whether: 
(i) it compiles without sorry and only depends on the three standard axioms (propext, Classical.choice, and Quot.sound), and
(ii)  the proofs of the statements have been formalized correctly, and
(iii) the statements themselves have been formalized correctly and faithfully, and
(iv) the formalization follows the actual arguments and reasoning steps that were used in the proofs in the write-up. That is, check that not a different proof has tacitly been formalized.
"

The initial formalization attempt already compiled without sorry, and depended only on the standard axioms propext, Classical.choice, and Quot.sound. However, for Proposition 3.1 it was not yet completely faithful to the way we wrote the proofs. In contrast, the version that is currently in the repository survived the scrutiny of adversarial checks (up to the small caveats described below). Due to the stricter requirements we imposed, the number of files and their sizes grew larger than perhaps necessary.

In the present state, adversarial LLM checks still produce some complaints when prompted to provide them, but we believe they are minor. For instance: 
(1) For some lines with asymptotic terms such as O_k((q^{-1}), Lean formalizes computations via a slightly different approach compared to the write-up.
(2) For the asymptotic analysis, the preprint chooses the largest prime not exceeding d^{1/2k}-1, while the Lean formalization chooses the prime in a different way,
(3) For the proof of Theorem 1.1, the preprint singles out the easy case $k=1$ by noting it (also) follows from complete graphs, while the Lean formalization absorbs it in the general argument.
(4) For the external results cited for use in Lemma 2.1, the proofs supplied by the Lean formalization do not necessarily correspond to the proofs in the cited sources.

Perhaps the most clear `gap' is that the external Theorem 7 (or the more accurate Theorem 10) from reference [8] (https://doi.org/10.1137/21M1437354) has not yet been formalized. The present paper only invokes that result for the claim that the bound from Corollary 1.2 is tight for bipartite graphs, and thus it has no consequences for any of the formally stated results (Theorem 1.1, Corollary 1.2, Lemma 2.1, Proposition 3.1 and Lemma 4.1).

The formalization was carried out in the final phase of the project, based on the version of August 3, 2026.


