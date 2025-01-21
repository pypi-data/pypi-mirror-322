from sentence_transformers import CrossEncoder

# Загружаем предобученную модель Cross-Encoder
model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2', max_length=512)

# Пример найденных релевантных контекстов и запроса
query = "What is Python?"
contexts = [
    "My first paragraph. That contains information",
    "Python is a programming language."
]

# Формируем пары запрос-контекст для оценки
pairs = [[query, context] for context in contexts]

# Получаем оценки для каждой пары
scores = model.predict(pairs)

# Сортируем контексты по убыванию оценки
ranked_contexts = [context for _, context in sorted(zip(scores, contexts), reverse=True)]

# Выводим результат
for i, context in enumerate(ranked_contexts):
    print(f"Rank {i+1}: {context}")