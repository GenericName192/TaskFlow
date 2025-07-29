import random
tips = [
    "Start your day with your toughest task. It sets the tone.",
    "Done is better than perfect — keep moving forward.",
    "Small progress is still progress. Celebrate it.",
    "Break big tasks into bite-sized pieces and conquer them.",
    "Lead by example. Your team mirrors your habits.",
    "Delegation isn’t weakness, it’s leadership.",
    "Review your goals every morning to stay aligned.",
    "If it takes less than 2 minutes, do it now.",
    "Overwhelmed? Prioritize just 3 key tasks for today.",
    "Be clear with your team—clarity drives results.",
    "Your task list is a reflection of your goals. Review it often.",
    "Progress > Perfection. Keep showing up.",
    "Check in with your subordinates regularly—support breeds productivity.",
    "Every task completed brings you closer to your vision.",
    "Silence distractions. Focus is your superpower.",
    "Set realistic deadlines—and stick to them.",
    "Take breaks. Rest fuels results.",
    "A clean task list leads to a clear mind.",
    "Your team’s success is your success. Empower them."
]


def get_tip():
    return random.choice(tips)
