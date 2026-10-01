# Zenodo description

[日本語](zenodo-description.ja.md)

Copy the title and description into a Software record and select **Apache License 2.0 (Apache-2.0)** in the license field. The repository includes the license text and attribution notice. No existing app DOI is asserted.

## Title

M-Anchor App V1: A Deterministic Gate for Containing Prompt-Induced Unauthorized Record Updates

## Description

M-Anchor App is a local Python application that separates AI-generated proposals from authoritative case-record updates. A deterministic gate checks the referenced state, externally admitted evidence, candidate transitions, and authority requests before saving a change. Its principle is: Model proposes; deterministic layer commits.

The V1 demonstration includes four fixed attack types (unsupported resolution, forged evidence admission, future-check bypass, and state-reference tampering), two controls, an optional model connection, and separate English and Japanese documentation with a bilingual interface. Input, proposal, decision, and read-back state can be inspected and exported. The source package includes reproduction instructions, validation records, and two original observation exports containing 20 entries and one entry, respectively.

The fixed observations show rejection of four invalid proposal types and acceptance of a supported update. Three model-route observations record one adversarial input that the model itself answered by preserving uncertainty, one valid no-change proposal, and one supported update saved from Version 1 to Version 2. The adversarial model example is not a gate rejection of an invalid model output.

“Attack neutralization” is limited here to blocking unauthorized case-record transitions at the gate. The app does not prevent all incorrect GPT text, establish evidence truth, control external tools, or demonstrate universal prompt-injection or jailbreak resistance. This is a software demonstration with inspectable evidence, not an independently certified security product. Python 3.10 or later is required; fixed scenarios need no model API key. This distribution is licensed under Apache-2.0, permitting commercial use, modification, and redistribution under its terms. The M-Anchor Framework is a related, separately versioned project.
