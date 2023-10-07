import numpy as np

num_vocabularies = 5
num_days = 7

Q = np.zeros((num_vocabularies, num_days))

learning_rate = 0.1
discount_factor = 0.9
exploration_prob = 0.3
num_episodes = 1000

def choose_action(Q, state, epsilon):
    if np.random.uniform(0, 1) < epsilon:
        return np.random.choice(num_days)
    else:
        return np.argmax(Q[state, :])


for episode in range(num_episodes):
    state = 0
    for _ in range(num_days):
        action = choose_action(Q, state, exploration_prob)

        reward = state * action

        Q[state, action] = (1 - learning_rate) * Q[state, action] + learning_rate * (
                    reward + discount_factor * np.max(Q[state, :]))

        state = action

best_num_vocabularies = np.argmax(Q, axis=0)
best_num_days = np.arange(num_days)

for day, vocab in enumerate(best_num_vocabularies):
    print(f"Ngày {day + 1}: {vocab} từ vựng")

for vocab, day in enumerate(best_num_days):
    print(f"{vocab} từ vựng: Ngày {day + 1} ôn tập")
