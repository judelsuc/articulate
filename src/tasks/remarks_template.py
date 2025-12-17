"""
Remarks template for user feedback and comments on generated articles.
"""


def create_remarks_template(topic: str, article_snippet: str = "") -> str:
    """
    Create a remarks template for the user to add their feedback
    
    Args:
        topic: The article topic
        article_snippet: Optional snippet from the article for reference
        
    Returns:
        Formatted remarks template
    """
    return f"""# Remarks & Feedback: {topic}

## Your Initial Assessment

**Overall Impression:**
- [ ] Excellent - Ready to post
- [ ] Good - Needs minor edits
- [ ] Okay - Needs rework
- [ ] Weak - Start over

**Key Strengths:**
(What works well in this article?)

1. 
2. 
3. 

**Areas for Improvement:**
(What could be better?)

1. 
2. 
3. 

---

## Content Feedback

### Headline
**Current:** (from plan.md)
**Your Thoughts:** 

**Suggested Alternative:**

### Hook/Opening
**Your Assessment:**

### Structure & Flow
**What's Working:**

**What Needs Adjustment:**

### Examples & Evidence
**Good Examples:**

**Missing Examples (add?):**

### Call-to-Action
**Current CTA Assessment:**

**Suggested CTA (if needed):**

---

## Tone & Voice

**Tone Assessment:**
- [ ] Too formal
- [ ] Just right
- [ ] Too casual

**Adjustments Needed:**

---

## LinkedIn-Specific

**Hashtags Review:**
**Current:** (from article)
**Your Suggestions:**

**Engagement Hooks:**
(What will make people comment?)

**Audience Fit:**
(Who is this for? Will they engage?)

---

## Final Edits

**Typos/Grammar:**
(List any fixes needed)

**Link/Citation Additions:**

**Personal Stories to Add:**

---

## Publish Decision

**Ready to Post:** [ ] Yes  [ ] No

**Publishing Date/Time Preference:**

**LinkedIn Post Strategy:**
(Include this in post? Share on newsletter? Both?)

---

## Notes for Next Article

**What Worked Well (repeat in future):**

**What to Avoid Next Time:**

**Topics to Explore:**

"""
