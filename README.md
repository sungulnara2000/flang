## Практикум №1 по курсу "Формальные языки и трансляции"
Даны регулярное выражение α в обратной польской записи, задающее язык L и слово u ∈ {a, b, c}. 
Найти длину самого длинного суффикса u, являющегося также суффиксом некоторого слова в L.

# Решение
1. Строим НКА по данному регулярному выражению. 
   Разбираем выражение с помощью стека: кладем на вершину новый автомат, который получен применением операции. В результате при корректом вводе на вершину стека лежит один элемент - требуемый НКА с ε-переходами.
2. Инвертируем все ребра НКА и меняем начальную вершину с завершающей.
3. Строим ДКА по НКА. 
   ε-замыкание состояния X - набор состояний, которые могут быть достигнуты из X только по ε-переходам, включая само состояние X
   3.1: Принимаем ε-замыкание для начального состояния НКА в качестве начального состояния ДКА.
   3.2: Находим состояния, в которые можно пройти из настоящего для каждого символа алфавита. Кладем их на стек, если они еще не встречались.
   3.3: Берем состояние с вершины.
   3.4: Повторяем Шаг 3.2 и Шаг 3.3, пока стек не пуст.
   3.5: Отмечаем состояния ДКА, которые содержат конечное состояние НКА, как конечные состояния ДКА.
4. Инвертируем слово u.
5. Идем по автомату начиная со стартовой вершины, пытаясь переходить по ребру, отмеченному текщей буквой слова u.
