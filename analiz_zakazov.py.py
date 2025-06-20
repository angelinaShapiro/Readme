import json
from collections import defaultdict

def analyze_orders(filename="orders_july_2023.json"):
    """
    Анализирует данные о заказах из JSON-файла и отвечает на вопросы о статистике заказов.

    Args:
        filename: Имя JSON-файла, содержащего данные о заказах.

    Returns:
        Словарь, содержащий ответы на вопросы.
    """

    try:
        with open(filename, "r", encoding='utf-8') as f:  # Добавил encoding='utf-8'
            orders = json.load(f)
    except FileNotFoundError:
        return "Ошибка: Файл не найден."
    except json.JSONDecodeError:
        return "Ошибка: Неверный формат JSON."

    # Инициализация переменных
    max_price = 0
    max_order_price = ''
    max_quantity = 0
    max_order_quantity = ''
    order_counts_by_date = defaultdict(int)
    user_order_counts = defaultdict(int)
    user_total_spending = defaultdict(float)  # Используем float для денежных значений
    total_price = 0
    total_quantity = 0
    order_count = 0

    # Обработка заказов
    for order_num, order_data in orders.items():
        date_str = order_data['date']
        user_id = order_data['user_id']
        quantity = order_data['quantity']
        price = order_data['price']

        # Обновляем количество заказов по дате
        order_counts_by_date[date_str] += 1

        # Обновляем количество заказов пользователя
        user_order_counts[user_id] += 1

        # Обновляем общую сумму покупок пользователя
        user_total_spending[user_id] += price

        # Обновляем общую цену и количество товаров
        total_price += price
        total_quantity += quantity
        order_count += 1

        # Находим самый дорогой заказ
        if price > max_price:
            max_order_price = order_num
            max_price = price

        # Находим заказ с наибольшим количеством товаров
        if quantity > max_quantity:
            max_order_quantity = order_num
            max_quantity = quantity

    # Находим день с наибольшим количеством заказов
    most_popular_date = max(order_counts_by_date, key=order_counts_by_date.get, default="N/A")

    # Находим пользователя с наибольшим количеством заказов
    most_active_user = max(user_order_counts, key=user_order_counts.get, default="N/A")

    # Находим пользователя с наибольшей общей стоимостью заказов
    top_spender = max(user_total_spending, key=user_total_spending.get, default="N/A")

    # Вычисляем среднюю стоимость заказа
    average_order_price = total_price / order_count if order_count > 0 else 0

    # Вычисляем среднюю стоимость товара
    average_item_price = total_price / total_quantity if total_quantity > 0 else 0

    results = {
        "most_expensive_order": max_order_price,
        "order_with_most_items": max_order_quantity,
        "busiest_date": most_popular_date,
        "most_active_user": most_active_user,
        "top_spender": top_spender,
        "average_order_price": average_order_price,
        "average_item_price": average_item_price,
    }

    return results


# Пример использования (предполагается, что orders_july_2023.json находится в том же каталоге)
if __name__ == "__main__":
    results = analyze_orders()

    if isinstance(results, str):  # Проверяем наличие сообщения об ошибке
        print(results)
    else:
        print(f"Номер самого дорого заказа за июль: {results['most_expensive_order']}")
        print(f"Номер заказа с самым большим количеством товаров: {results['order_with_most_items']}")
        print(f"В какой день в июле было сделано больше всего заказов: {results['busiest_date']}")
        print(f"Какой пользователь сделал самое большое количество заказов за июль: {results['most_active_user']}")
        print(f"У какого пользователя самая большая суммарная стоимость заказов за июль: {results['top_spender']}")
        print(f"Какая средняя стоимость заказа была в июле: {results['average_order_price']:.2f}")
        print(f"Какая средняя стоимость товаров в июле: {results['average_item_price']:.2f}")