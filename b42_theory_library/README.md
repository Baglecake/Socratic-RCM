# Theoretical Knowledge Base

This directory contains lecture notes and theoretical materials that serve as the knowledge base for the Socratic RCM system. These materials were created by Professor Daniel Silver (University of Toronto) for the B42 Chatstorm assignment.

## Contents

| File | Theorist | Key Concepts |
|------|----------|--------------|
| [marx_theory.txt](marx_theory.txt) | Karl Marx | Alienation, class conflict, labor exploitation, surplus value |
| [wollstonecraft_theory.txt](wollstonecraft_theory.txt) | Mary Wollstonecraft | Non-domination, rational agency, gender equality, education |
| [smith_theory.txt](smith_theory.txt) | Adam Smith | Self-interest, market behavior, division of labor, moral sentiments |
| [tocqueville_theory.txt](tocqueville_theory.txt) | Alexis de Tocqueville | Democratic participation, civic virtue, tyranny of the majority |

## Theoretical Frameworks

The PRAR workflow supports five theoretical framework options that draw on combinations of these theorists:

| Option | Framework | Theorists | Concept A | Concept B |
|--------|-----------|-----------|-----------|-----------|
| A | Class Conflict / Alienation | Marx, Wollstonecraft | Alienation | Non-domination |
| B | Democratic Participation | Tocqueville, Smith | Civic virtue | Self-interest |
| C | Gender and Power | Wollstonecraft, Marx | Domination | Exploitation |
| D | Economic Rationality | Smith, Tocqueville | Market behavior | Democratic norms |
| E | Custom | User-defined | User-defined | User-defined |

## Usage in the System

### PRAR Workflow

During the 112-step PRAR workflow, the system references these materials to:
- Guide theoretical framework selection (Phase 1)
- Validate concept definitions against source materials
- Ensure agent personas align with theoretical grounding

### Social RL Framework

In Social RL simulations, theoretical concepts inform:
- **Context Injection**: Concept manifestations derived from theoretical frameworks
- **Feedback Extraction**: Alignment scores measure adherence to theoretical principles
- **Process Retrieval**: Reasoning policies grounded in theoretical constraints

### Knowledge Base References

Runtime files use notation like `KB[5]`, `KB[6]`, etc. to reference specific theory files:
- `KB[5]`: marx_theory.txt
- `KB[6]`: wollstonecraft_theory.txt
- `KB[7]`: smith_theory.txt
- `KB[8]`: tocqueville_theory.txt

## Academic Context

These materials support the pedagogical goal of the RCM system: scaffolding student understanding of classical sociological and political theory through Socratic questioning rather than content generation.

The system enforces that all theoretical references derive exclusively from these provided lecture materials, ensuring consistency and academic integrity.

## See Also

- [prar/README.md](../prar/README.md) - PRAR methodology and theoretical options
- [literature/README.md](../literature/README.md) - Academic literature on AI pedagogy
- [social_rl/README.md](../social_rl/README.md) - How theory informs Social RL
