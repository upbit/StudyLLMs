@Claude First, some basic Stable Diffusion prompting rules for you to better understand the syntax. The parentheses are there for grouping prompt words together, so that we can set uniform weight to multiple words at the same time. Notice the ":1.2" in (masterpiece, best quality, absurdres:1.2), it means that we set the weight of both "masterpiece" and "best quality" to 1.2. The parentheses can also be used to directly increase weight for single word without adding ":WEIGHT". For example, we can type ((masterpiece)), this will increase the weight of "masterpiece" to 1.21. This basic rule is imperative that any parentheses in a set of prompts have purpose, and so they must not be remove at any case. Conversely, when brackets are used in prompts, it means to decrease the weight of a word. For example, by typing "[bird]", we decrease the weight of the word "bird" by 1.1.

Now, I've develop a prompt template to use generate character portraits in Stable Diffusion. Here's how it works. Every time user sent you "CHAR prompts", you should give prompts that follow below format:
CHAR: [pre-defined prompts], [location], [time], [weather], [gender], [skin color], [photo type], [pose], [camera position], [facial expression], [body feature], [skin feature], [eye color], [outfit], [hair style], [hair color], [accessories], [random prompt],

[pre-defined prompts] are always the same, which are "RAW, (masterpiece, best quality, photorealistic, absurdres, 8k:1.2), best lighting, complex pupils, complex textile, detailed background". Don't change anything in [pre-defined prompts], meaning that you SHOULD NOT REMOVE OR MODIFY the parentheses since their purpose is for grouping prompt words together so that we can set uniform weight to them;
[location] is the location where character is in, can be either outdoor location or indoor, but need to be specific;
[time] refers to the time of day, can be "day", "noon", "night", "evening", "dawn" or "dusk";
[weather] is the weather, for example "windy", "rainy" or "cloudy";
[gender] is either "1boy" or "1girl";
[skin color] is the skin color of the character, could be "dark skin", "yellow skin" or "pale skin";
[photo type] can be "upper body", "full body", "close up", "mid-range", "Headshot", "3/4 shot" or "environmental portrait";
[pose] is the character's pose, for example, "standing", "sitting", "kneeling" or "squatting" ...;
[camera position] can be "from top", "from below", "from side", "from front" or "from behind";
[facial expression] is the expression of the character, you should give user a random expression;
[body feature] describe how the character's body looks like, for example, it could be "wide hip", "large breasts" or "sexy", try to be creative;
[skin feature] is the feature of character's skin. Could be "scar on skin", "dirty skin", "tanned mark", "birthmarks" or other skin features you can think of;
[eye color] is the pupil color of the character, it can be of any color as long as the color looks natural on human eyes, so avoid colors like pure red or pure black;
[outfit] is what character wears, it should include at least the top wear, bottom wear and footwear, for example, "crop top, shorts, sneakers", the style of outfit can be any, but the [character gender] should be considered;
[hair style] is the hairstyle of the character, [character gender] should be taken into account when setting the hairstyle;
[hair color] can be of any color, for example, "orange hair", "multi-colored hair";
[accessories] is the accessory the character might wear, can be "chocker", "earrings", "bracelet" or other types of accessory;
[random prompt] will test your creativity, put anything here, just remember that you can only use nouns in [random prompt], the number of [random prompt] can be between 1 to 4. For example, you could give "campfire", but you can also give "shooting star, large moon, fallen leaves". Again, be creative with this one.

Do not use markdown syntax in prompts, do not use capital letter and keep all prompt words in the same line. Respond with "Ok, got it." to start prompting with us.