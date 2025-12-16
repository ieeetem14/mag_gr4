import streamlit as st

# Używamy st.session_state do przechowywania danych
# Streamlit automatycznie zachowuje stan między interakcjami.

def initialize_inventory():
    """Inicjalizuje listę produktów w stanie sesji, jeśli jeszcze nie istnieje."""
    if 'inventory' not in st.session_state:
        st.session_state.inventory = [] # Pusta lista do przechowywania nazw produktów

def add_product(product_name):
    """Dodaje produkt do magazynu, jeśli nazwa nie jest pusta."""
    if product_name and product_name not in st.session_state.inventory:
        st.session_state.inventory.append(product_name)
        st.success(f"Dodano produkt: **{product_name}**")
    elif product_name in st.session_state.inventory:
        st.warning(f"Produkt **{product_name}** jest już w magazynie.")
    else:
        st.warning("Nazwa produktu nie może być pusta.")

def remove_product(product_name):
    """Usuwa produkt z magazynu."""
    if product_name in st.session_state.inventory:
        st.session_state.inventory.remove(product_name)
        st.info(f"Usunięto produkt: **{product_name}**")
    else:
        st.error(f"Produkt **{product_name}** nie został znaleziony w magazynie.")

# --- Główna logika aplikacji Streamlit ---

st.set_page_config(page_title="Prosta Aplikacja Magazynowa", layout="wide")
st.title("📦 Prosta Lista Magazynowa")
st.markdown("Aplikacja pozwala na dodawanie i usuwanie nazw produktów.")

# 1. Inicjalizacja stanu
initialize_inventory()

# --- Sekcja Dodawania Produktu ---
st.header("➕ Dodaj Produkt")
col1, col2 = st.columns([3, 1])

with col1:
    new_product_name = st.text_input("Wpisz nazwę produktu:", key="new_product_input")

with col2:
    # Dodajemy odstęp, aby przycisk był wyrównany z polem tekstowym
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Dodaj", use_container_width=True):
        add_product(new_product_name.strip())
        # Opcjonalnie: można wyczyścić pole tekstowe po dodaniu
        # st.session_state.new_product_input = "" 


# --- Sekcja Usuwania Produktu ---
if st.session_state.inventory:
    st.header("🗑️ Usuń Produkt")
    
    # Wybieranie produktu do usunięcia z listy dostępnych
    product_to_remove = st.selectbox(
        "Wybierz produkt do usunięcia:",
        options=st.session_state.inventory,
        key="remove_product_select"
    )
    
    if st.button("Usuń Wybrany Produkt", type="primary"):
        remove_product(product_to_remove)
else:
    st.markdown("---")
    st.warning("Brak produktów w magazynie do usunięcia.")


# --- Sekcja Wyświetlania Magazynu ---
st.markdown("---")
st.header("📋 Aktualny Magazyn")

if st.session_state.inventory:
    # Wyświetlenie listy produktów w formie uporządkowanej
    inventory_df = st.session_state.inventory
    
    # Użycie st.dataframe dla ładniejszego wyświetlenia
    st.dataframe(
        {"Nazwa Produktu": inventory_df}, 
        use_container_width=True,
        hide_index=True
    )
    st.markdown(f"**Liczba unikalnych produktów:** {len(st.session_state.inventory)}")
else:
    st.info("Magazyn jest obecnie pusty.")
