#!/usr/bin/env python3
"""
Email Style Templates for Different Approaches
Each style has its own personality and conversion strategy
"""

from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class EmailStyle:
    name: str
    description: str
    instructions: str
    example_subject: str
    example_structure: str

# Style Templates
EMAIL_STYLES = {
    "professional": EmailStyle(
        name="Professional Problem-Solution",
        description="Classic B2B approach. Clear value prop, professional tone, structured format.",
        instructions="""
You are an exceptional sales development representative creating professional outreach emails.

TONE & STRUCTURE:
- Professional but personable
- Clear problem → solution → benefit structure
- Proper capitalization and punctuation
- 100-150 words maximum
- Formal subject lines that create curiosity

FORMAT:
- Greeting: "Hi [Name]" or "Dear [Name]"
- Hook: Reference their company/role/recent activity
- Problem: Identify a challenge they likely face
- Solution: How we solve it (with case study proof)
- CTA: Clear meeting request
- Professional sign-off

EXAMPLE PATTERNS:
- "I noticed [specific activity]. Many [their role] struggle with [problem]."
- "Congrats on [achievement]. As you scale, [challenge] often becomes critical."
- "Your recent [activity] suggests [insight]. We help companies like yours [outcome]."

SUBJECT LINES:
- "[Benefit] for [Company]"
- "Quick question about [specific topic]"
- "[Competitor/Peer] + [Company] partnership?"
        """,
        example_subject="Scaling Your AI Consulting Pipeline",
        example_structure="""
Hi [Name],

Noticed your recent [specific achievement/activity]. Impressive work.

Many [role] at your stage face [specific challenge]. It often means [pain point].

We recently helped [similar company] achieve [specific metric] through [brief solution]. The key was [differentiator].

Worth a brief call to discuss how this could work for [company]?

Best regards,
[Your name]
        """
    ),
    
    "pattern_interrupt": EmailStyle(
        name="Pattern Interrupt",
        description="Modern 2026 style. Lowercase, curiosity gaps, peer proof, mobile-optimized.",
        instructions="""
You write outbound emails that break through noise using pattern interrupts and curiosity.

2026 PRINCIPLES:
- All lowercase (subject and body)
- Pattern interrupts: "weird question" "quick q" "random but"
- Mobile-first: short lines, no paragraphs
- Specific numbers: "47%" not "many"
- Time specificity: "12 min tuesday" not "15 minutes"
- Peer proof: "3 ex-meta pms" not "many clients"

PSYCHOLOGY:
- Start with "noticed" + ONE specific thing
- Agitate universal anxiety (not company-specific)
- Create curiosity gaps (don't explain everything)
- Keep it general enough to be relatable
- PS line: short callback to something they said

FORMAT:
- No formal greeting (jump right in)
- 2-3 word sentences OK
- Lots of line breaks
- Contrast structure: "not X but Y"
- Casual sign-off (just name)

AVOID:
- Capital letters (except names/acronyms)
- Periods at line ends
- Corporate speak
- Multiple paragraphs
- Explaining your solution
        """,
        example_subject="quick q about your roblox exit",
        example_structure="""
noticed [ONE specific thing - acquisition/role/post]

weird question - [universal challenge they face]?

[peer group] just [achieved outcome] using [simple method]

not [old way]
but [new way]

[one impressive metric]

worth [X] min [day] to see [deliverable]?

[name]
[link]

ps - [short callback]
        """
    ),
    
    "casual_conversational": EmailStyle(
        name="Casual Conversational", 
        description="Friendly peer-to-peer tone. Like texting a colleague you respect.",
        instructions="""
Write like you're reaching out to a peer you admire. Casual but respectful.

TONE:
- Conversational, like a Slack DM
- Use contractions (you're, I've, didn't)
- Natural enthusiasm without being salesy
- Mix of proper case and lowercase
- 80-120 words max

STRUCTURE:
- Start with "Hey [Name]" or just "[Name],"
- Personal observation or genuine compliment
- Relatable problem/question
- How we're solving it + quick proof
- Soft CTA: "Interested?" "Want to chat?"

PERSONALITY:
- Show genuine interest in their work
- Be humble about your solution
- Use "we/us" not "I" 
- Include personality (excited, curious, impressed)
- Natural speech patterns

EXAMPLES:
- "Hey [Name]! Just read your post about..."
- "Been following your work on [topic] - super interesting approach"
- "Quick thought after seeing your [achievement]..."
        """,
        example_subject="Loved your take on [topic]",
        example_structure="""
Hey [Name]!

Just saw your [specific post/news] about [topic] - really resonated with the part about [specific detail].

Been thinking about this exact problem lately. We're helping [peer companies] crack this by [simple explanation]. One founder just [specific win].

The approach is pretty different from [status quo]. Happy to share what's working if you're curious?

Cheers,
[Name]

P.S. - [Genuine personal comment or question]
        """
    ),
    
    "value_first": EmailStyle(
        name="Value-First Insight",
        description="Lead with valuable insight or data. Position as helpful expert sharing knowledge.",
        instructions="""
Lead with value. Share an insight that makes them think differently about their business.

APPROACH:
- Start with valuable insight/data
- Connect insight to their specific situation
- Soft pitch at end (almost optional)
- Position as expert helping expert
- 100-130 words

STRUCTURE:
- Subject: The insight itself
- Opening: Jump into the insight/data
- Context: Why this matters for them specifically
- Proof: Quick case study or metric
- Soft CTA: "Happy to share more"

VALUE TYPES:
- Industry trend they should know
- Competitive intelligence
- Method that's working for peers
- Counter-intuitive finding
- Specific tactic with proof

TONE:
- Authoritative but not condescending
- Generous with knowledge
- Peer-level expertise
- Focus on their success
        """,
        example_subject="87% of AI consultants miss this pricing opportunity",
        example_structure="""
Hi [Name],

Quick insight from analyzing 50+ independent AI consultants: 87% undercharge by 40-60% because they position as "freelancers" not "advisors."

Noticed you recently [specific transition]. The consultants crushing it right now frame their expertise differently - one changed positioning and went from $5k to $25k engagements overnight.

The shift is subtle but powerful. Instead of "I can help with AI," it's "I've shipped [specific achievement] at scale."

We've codified this approach after seeing it work repeatedly. Happy to share the exact framework if useful.

Best,
[Name]

[Link to resource or calendar]
        """
    ),
    
    "challenge_based": EmailStyle(
        name="Challenge-Based",
        description="Open with a challenging question or statement. Provocative but respectful.",
        instructions="""
Start with a respectful challenge that makes them think. Not aggressive, but thought-provoking.

PRINCIPLES:
- Open with challenging question/statement
- Back it up with data or peer examples
- Show you understand their world
- Offer different perspective
- 90-120 words

CHALLENGE TYPES:
- Question an assumption
- Point out missed opportunity
- Highlight competitive gap
- Challenge status quo approach
- Present surprising data

TONE:
- Confident but not arrogant
- Respectful challenger
- Data-driven points
- Solution-oriented
- Peer-to-peer dynamic

STRUCTURE:
- Subject: The challenge itself
- Opening: Direct challenge/question
- Context: Why this matters now
- Proof: Data or peer example
- CTA: "Let's discuss" / "Thoughts?"
        """,
        example_subject="Is your expertise worth 10x more than you're charging?",
        example_structure="""
[Name],

Real question: Why charge $200/hour for expertise that saves companies millions?

Just saw three AI consultants 10x their rates after repositioning from "contractor" to "strategic advisor." Same work, different framing.

Your [specific achievement] alone is worth more than most consultants' entire portfolio. But generic outreach undermines that value.

We help technical experts command premium rates through positioning that matches their impact. Curious if you've thought about this?

[Name]
[Quick link]
        """
    )
}

def get_style_prompt(style_name: str, data: Dict[str, Any]) -> str:
    """
    Generate style-specific prompt instructions
    
    Args:
        style_name: Name of the style to use
        data: Prospect and company data
        
    Returns:
        Formatted prompt with style instructions
    """
    style = EMAIL_STYLES.get(style_name, EMAIL_STYLES["professional"])
    
    prompt = f"""
{style.instructions}

<prospect>
Name: {data.get('firstName')} {data.get('lastName')}
Title: {data.get('title', 'Professional')}
Company: {data.get('companyName')}
Industry: {data.get('industry', 'Technology')}
Recent: {data.get('activity')}
LinkedIn: {data.get('linkedinURL')}
</prospect>

<sender>
{data.get('senderName')} from {data.get('senderCompany')}
Meeting link: {data.get('meetingLink')}
</sender>

<our_value>
{data.get('caseStudy')}
Target: {data.get('ICP')}
</our_value>

Write an email in the {style.name} style. Follow the format and tone guidelines EXACTLY.

OUTPUT FORMAT:
Subject: [write subject line in the style shown]

[write email body following the exact style format]

IMPORTANT: 
- Follow the style instructions precisely
- Match the example tone and structure
- Do NOT add any explanations or analysis
- For pattern_interrupt style: ALL lowercase, no formal punctuation, lots of line breaks
"""
    
    return prompt

def list_available_styles() -> Dict[str, str]:
    """Return available styles with descriptions"""
    return {
        name: style.description 
        for name, style in EMAIL_STYLES.items()
    }

# Example usage
if __name__ == "__main__":
    print("🎯 Available Email Styles:\n")
    for name, description in list_available_styles().items():
        print(f"{name}: {description}")
        print(f"Example subject: {EMAIL_STYLES[name].example_subject}\n")