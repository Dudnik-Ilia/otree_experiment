import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


np.random.seed(42)
n_participants = 100

# # Generating data for treatment check
# data = {
#     "Treatment": np.repeat(["High-Ego", "Low-Ego"], n_participants),
#     "relevance_replacement": np.concatenate([np.random.randint(2, 7, n_participants), np.random.randint(1, 5, n_participants)]),
#     "relevance_involvement": np.concatenate([np.random.randint(3, 8, n_participants), np.random.randint(2, 5, n_participants)]),
#     "relevance_ai_role": np.concatenate([np.random.randint(3, 6, n_participants), np.random.randint(2, 5, n_participants)])
# }

# df = pd.DataFrame(data)

# # Plotting
# sns.set(style="whitegrid")
# fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# # Perceived relevance of AI replacing human jobs
# sns.boxplot(ax=axes[0], data=df, x="Treatment", y="relevance_replacement", palette="pastel")
# axes[0].set_title("Perceived Relevance of AI Replacing Human Jobs")
# axes[0].set_ylabel("Rating (1-7)")

# # Self-reported effort
# sns.boxplot(ax=axes[1], data=df, x="Treatment", y="relevance_involvement", palette="pastel")
# axes[1].set_title("Self-Reported Effort in the Task")
# axes[1].set_ylabel("Rating (1-7)")

# # Perceived AI role
# sns.boxplot(ax=axes[2], data=df, x="Treatment", y="relevance_ai_role", palette="pastel")
# axes[2].set_title("Perceived Likelihood of Central AI Role")
# axes[1].set_ylabel("Rating (1-7)")

# plt.tight_layout()
# plt.show()

# Generating data for regression analysis
initial_belief = np.random.uniform(40, 60, 2 * n_participants)
task_performance = np.random.uniform(40, 80, n_participants * 2)
treatment = np.array([1] * n_participants + [0] * n_participants)

# Introduce optimistic bias in final belief updates for the High-Ego treatment
final_belief = initial_belief + 0.2 * (task_performance - initial_belief) + treatment * np.random.uniform(5, 10, 2 * n_participants)

# Create DataFrame
df = pd.DataFrame({
    "InitialBelief": initial_belief,
    "TaskPerformance": task_performance,
    "Treatment": ["High-Ego" if t == 1 else "Low-Ego" for t in treatment],
    "FinalBelief": final_belief
})

# Visualization
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x="InitialBelief", y="FinalBelief", hue="Treatment", style="Treatment")
plt.plot([40, 60], [40, 60], 'k--', label="No update baseline")
plt.xlabel("Initial Belief")
plt.ylabel("Final Belief")
plt.title("Belief Updating in High-Ego vs. Low-Ego Treatment")
plt.legend(title="Treatment Condition")
plt.tight_layout()
plt.show()
