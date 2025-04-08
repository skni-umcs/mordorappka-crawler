import requests
from typing import List, Optional
from dacite import from_dict
from util_types import Activity
import dacite


def get_activity(url: str, id: int) -> Optional[List[Activity]]:
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    # Ciało zapytania zawierające id
    payload = {
        "id": id
    }
    
    # Wysłanie zapytania GET z ciałem w formacie JSON
    response = requests.get(
        url,
        headers=headers,
        json=payload
    )
    
    # Sprawdzenie, czy zapytanie było udane
    if response.status_code != 200:
        print(f"❌ Błąd API: {response.status_code}")
        return None
        
    try:
        # Parsowanie odpowiedzi JSON
        data = response.json()
        
        # Sprawdzamy czy dane zawierają oczekiwaną strukturę
        if "result" not in data or "array" not in data["result"]:
            print("❌ Nieoczekiwana struktura danych z API.")
            return None
            
        # Pobieramy tablicę aktywności
        activities_data = data["result"]["array"]
        
        if not activities_data:
            print("❌ Nie znaleziono aktywności.")
            return None
            
        # Tworzenie listy obiektów Activity z danych JSON
        activities = []
        for activity_data in activities_data:
            try:
                # Konwersja danych JSON do obiektu Activity przy użyciu dacite
                activity = from_dict(
                    data_class=Activity, 
                    data=activity_data,
                    config=dacite.Config(check_types=False)
                )
                activities.append(activity)
            except Exception as e:
                print(f"❌ Błąd przetwarzania aktywności: {str(e)}")
                print(f"Problematyczne dane: {activity_data}")
                continue
        
        if not activities:
            print("❌ Nie udało się przetworzyć żadnej aktywności.")
            return None
            
        return activities
    except Exception as e:
        print(f"❌ Błąd podczas przetwarzania danych: {str(e)}")
        return None