# String Element Manipulation: Problem-Solving Guide

A focused workout guide for mastering string manipulation patterns in Python.

---

## Overview: The Mental Framework

Before diving into individual problems, internalize this general approach:

### Step 1: Identify the Operation Type
| Type | Key Question | Common Patterns |
|------|--------------|-----------------|
| **Reordering** | How do positions change? | Two pointers, reverse iteration, slicing |
| **Transformation** | What happens to each element? | Character mapping, ASCII math, lookup tables |
| **Building/Insertion** | What goes between/around elements? | Join operations, accumulator patterns |
| **Searching** | What am I looking for and where? | Index tracking, sliding window, find() |
| **Counting** | How many of what? | Hash maps, Counter, frequency arrays |

### Step 2: Choose Your Accumulation Strategy
Since Python strings are **immutable**, you're always building something new:

```
Option A: List accumulation → ''.join(result_list)
Option B: String concatenation (less efficient for many operations)
Option C: Built-in methods (slicing, replace, etc.)
```

### Step 3: Identify State Requirements
- Do I need to track position/index?
- Do I need to remember what I've seen before?
- Does the current operation depend on previous operations?

---

## Problem 1: Reverse String

### Problem Essence
Transform `"hello"` → `"olleh"` (mirror all character positions)

### Thinking Prompts

**What does "reverse" mean positionally?**
- Character at index `0` goes to index `n-1`
- Character at index `i` goes to index `n-1-i`
- What's the relationship between original and new positions?

**What are your options for reversing?**

| Approach | How It Works | Think About... |
|----------|--------------|----------------|
| Python slicing | Uses slice syntax | What slice notation produces a reverse? |
| Backward iteration | Build from end to start | How do you iterate in reverse? |
| Two pointers | Swap from outside in | How would this work if strings were mutable? |
| Built-in methods | Use existing functions | What does `reversed()` return? |

**Key Implementation Questions:**
- If iterating backward, what's your range? `range(?, ?, ?)`
- If using two pointers conceptually, where do they start?

### Edge Cases to Handle
- [ ] Empty string `""`
- [ ] Single character `"a"`
- [ ] String with spaces `"a b c"`
- [ ] String with special characters `"hello!@#"`

### Complexity Targets
- **Time:** O(n) - must visit each character once
- **Space:** O(n) - need space for the new string

### Hint (if stuck)
Python slicing with a step of `-1` traverses backward. What does `s[start:stop:step]` do when step is negative?

---

## Problem 2: Add Spacing to String

### Problem Essence
Transform `"ABC"` → `"A B C"` (insert space between adjacent characters)

### Thinking Prompts

**What's the mathematical relationship?**
- Input has `n` characters
- Output has `n` characters + `?` spaces
- How many "gaps" exist between `n` items?

**What pattern is this?**
This is a classic "insert delimiter between elements" problem. Where else have you seen this pattern?

**Approaches to Consider:**

| Approach | Key Insight |
|----------|-------------|
| Join operation | What does `delimiter.join(iterable)` do? |
| Manual building | Add character, then conditionally add space |
| List comprehension | Can you build the spaced version in one expression? |

**Key Implementation Questions:**
- If building manually, when do you add a space and when don't you?
- What does `" ".join("hello")` produce? (Try it mentally first)

### Edge Cases to Handle
- [ ] Empty string `""` → `""`
- [ ] Single character `"A"` → `"A"` (no spaces to add!)
- [ ] Already has spaces `"A B"` → `"A   B"` (space becomes surrounded by spaces)

### Complexity Targets
- **Time:** O(n)
- **Space:** O(n) for the result (roughly 2n-1 characters)

### Hint (if stuck)
A string is iterable. The `join()` method works on any iterable, inserting the delimiter between each element of that iterable.

---

## Problem 3: String Alphabetic Shift

### Problem Essence
Transform each letter to its successor: `"abc"` → `"bcd"`, with `"z"` → `"a"`

### Thinking Prompts

**How do you represent "next letter" computationally?**
- Characters have numeric representations (ASCII/Unicode)
- What's `ord('a')`? What's `chr(97)`?
- What's the relationship between `ord('a')` and `ord('b')`?

**How does wrapping work?**
- `'z'` should become `'a'`
- This is **modular arithmetic** - what operation creates cycles?
- If the alphabet has 26 letters, and you're at position 25 (z), what's `(25 + 1) % 26`?

**The Formula Pattern:**
```
new_char = chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
```
Break this down piece by piece:
1. `ord(char) - ord('a')` → converts 'a'-'z' to 0-25
2. `+ shift` → moves forward in alphabet
3. `% 26` → wraps around if past 'z'
4. `+ ord('a')` → converts back to ASCII value
5. `chr(...)` → converts ASCII to character

### Edge Cases to Handle
- [ ] Empty string `""`
- [ ] Contains 'z' → must wrap to 'a'
- [ ] All same letter `"aaaa"` → `"bbbb"`

### Complexity Targets
- **Time:** O(n) - process each character once
- **Space:** O(n) - store the result

### Hint (if stuck)
The modulo operator `%` is your friend for circular/wrapping behavior. If you have values 0-25 and add 1, what does `% 26` do to the result when you're at 25?

---

## Problem 4: Count Target String

### Problem Essence
Count **non-overlapping** occurrences of target in string.
`"aaaa"` with target `"aa"` → `2` (not 3!)

### Thinking Prompts

**What does "non-overlapping" mean for your search?**
- If you find a match at index `i`, where do you search next?
- Overlapping: next search at `i + 1`
- Non-overlapping: next search at `i + len(target)`

**Two Approaches:**

| Approach | Method | Consideration |
|----------|--------|---------------|
| Built-in | `str.count()` | Does it handle overlapping or non-overlapping? |
| Manual | Loop with `find()` | You control where to search next |

**Key Implementation Questions:**
- What does `string.find(target, start_index)` return?
- What return value signals "not found"?
- After finding at index `i`, what should your new start index be?

**Manual Approach Skeleton:**
```
count = 0
position = 0
while position <= len(string) - len(target):
    found_at = string.find(target, position)
    if found_at == ???:  # What indicates not found?
        break
    count += 1
    position = ???  # Where do you search next?
return count
```

### Edge Cases to Handle
- [ ] Empty target `""` → return 0
- [ ] Target longer than string → return 0
- [ ] No occurrences → return 0
- [ ] Overlapping potential: `"111"` with target `"11"` → 1

### Complexity Targets
- **Time:** O(n × m) worst case where n = string length, m = target length
- **Space:** O(1) auxiliary (just tracking count and position)

### Hint (if stuck)
Python's built-in `str.count()` already handles non-overlapping counting. But understanding the manual approach with `find()` is valuable for variations of this problem.

---

## Problem 5: Remove Target String F Times

### Problem Essence
Remove first `f` occurrences of target, BUT only if target appears at least `f` times.

### Thinking Prompts

**This has a precondition!**
Before doing ANY removals, you must verify the target appears ≥ f times.
- How can you count occurrences? (You just solved this!)
- What do you return if the precondition fails?

**How does removal affect subsequent searches?**
After removing a substring:
- The string gets shorter
- Indices shift
- The "next" occurrence might now be at a different position

**Two-Phase Approach:**
```
Phase 1: Verify - count occurrences, check if >= f
Phase 2: Execute - remove f occurrences one at a time
```

**Key Implementation Questions:**
- How do you remove a substring at a known index?
- What does `string.replace(target, '', count)` do?
- Alternative: `string[:index] + string[index + len(target):]`

**Approaches:**

| Approach | Method | Consideration |
|----------|--------|---------------|
| Replace with count | `str.replace(old, new, count)` | Does this do exactly f replacements? |
| Find and slice | Find index, slice around it | More control, more code |

### Edge Cases to Handle
- [ ] `f = 0` → return original string (no removals requested)
- [ ] Target appears fewer than `f` times → return original unchanged
- [ ] `f` removals result in empty string → return `""`
- [ ] Removal creates new match: `"aabcbc"` remove `"abc"` once → `"abc"` (new target appears!)

### Complexity Targets
- **Time:** O(f × n) for f removals on string of length n
- **Space:** O(n) for the result string

### Hint (if stuck)
`str.replace(old, new, count)` takes an optional third argument that limits replacements. Check if this matches the problem's requirements exactly.

---

## Problem 6: Find Most Frequent Character

### Problem Essence
Find the character that appears most often in the string.

### Thinking Prompts

**What data structure is built for counting?**
- Hash map / dictionary: `{char: count}`
- Python's `collections.Counter` is purpose-built for this

**Two-Phase Pattern:**
```
Phase 1: Count everything
Phase 2: Find the maximum
```

**Approaches for Phase 1 (Counting):**

| Approach | Code Pattern |
|----------|--------------|
| Manual dict | `counts = {}; for char in s: counts[char] = counts.get(char, 0) + 1` |
| defaultdict | `counts = defaultdict(int); for char in s: counts[char] += 1` |
| Counter | `counts = Counter(s)` |

**Approaches for Phase 2 (Find Max):**

| Approach | Code Pattern |
|----------|--------------|
| Loop through dict | Track max_count and max_char as you iterate |
| max() with key | `max(counts, key=counts.get)` |
| Counter method | `counts.most_common(1)[0][0]` |

**Key Implementation Questions:**
- What does `max(dictionary)` return by default?
- How does the `key` parameter change what `max()` compares?
- What does `dict.get(key)` return?

### Edge Cases to Handle
- [ ] Single character string → return that character
- [ ] All same character → return that character
- [ ] Spaces as most frequent → return `" "`

### Complexity Targets
- **Time:** O(n) to count + O(k) to find max, where k = unique characters → O(n) overall
- **Space:** O(k) for the frequency map, where k ≤ n

### Hint (if stuck)
`max(iterable, key=function)` returns the item from iterable for which `function(item)` is largest. If you have a dictionary `d`, what does `max(d, key=d.get)` find?

---

## Quick Reference: Python String Methods

| Method | What It Does | Example |
|--------|--------------|---------|
| `s[::-1]` | Reverse via slicing | `"abc"[::-1]` → `"cba"` |
| `"x".join(iterable)` | Join with delimiter | `" ".join("ab")` → `"a b"` |
| `s.find(sub, start)` | Find index or -1 | `"hello".find("l")` → `2` |
| `s.count(sub)` | Count non-overlapping | `"aaa".count("aa")` → `1` |
| `s.replace(old, new, n)` | Replace up to n times | `"aaa".replace("a", "b", 2)` → `"bba"` |
| `ord(c)` | Character → ASCII int | `ord('a')` → `97` |
| `chr(n)` | ASCII int → character | `chr(98)` → `'b'` |

---

## Practice Checklist

For each problem, verify you can:
- [ ] Explain your approach before coding
- [ ] Identify time and space complexity
- [ ] Handle all edge cases
- [ ] Write clean, readable code
- [ ] Consider at least one alternative approach

Good luck with your workout! 💪
