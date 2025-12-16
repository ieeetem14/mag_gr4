import streamlit as st

# --- Funkcje Zarządzania Magazynem ---

def initialize_inventory():
    """Inicjalizuje listę produktów w st.session_state, jeśli nie jest jeszcze ustawiona."""
    if 'inventory' not in st.session_state:
        st.session_state.inventory = [] 

def add_product(product_name):
    """Dodaje produkt do magazynu, sprawdzając unikalność i pustą nazwę."""
    product_name = product_name.strip()
    if not product_name:
        st.warning("Nazwa produktu nie może być pusta.")
        return

    if product_name not in st.session_state.inventory:
        st.session_state.inventory.append(product_name)
        st.session_state.inventory.sort() # Sortowanie alfabetyczne dla lepszej organizacji
        st.success(f"Dodano produkt: **{product_name}**")
    else:
        st.warning(f"Produkt **{product_name}** jest już w magazynie.")

def remove_product(product_name):
    """Usuwa produkt z magazynu."""
    if product_name in st.session_state.inventory:
        st.session_state.inventory.remove(product_name)
        st.info(f"Usunięto produkt: **{product_name}**")
    else:
        st.error(f"Wystąpił błąd: Produkt **{product_name}** nie został znaleziony.")

# --- Główna Logika Streamlit ---

st.set_page_config(page_title="Prosta Aplikacja Magazynowa", layout="wide")
st.title("📦 Prosta Lista Magazynowa (Streamlit)")
st.markdown("Aplikacja do zarządzania nazwami produktów, bez zapisywania do pliku.")

# 1. Inicjalizacja stanu (session_state)
initialize_inventory()

# --- Sekcja Dodawania Produktu ---
st.header("➕ Dodawanie Produktu")
col_add, col_button_add = st.columns([3, 1])

with col_add:
    new_product_name = st.text_input("Wpisz nazwę produktu:", key="new_product_input", label_visibility="collapsed", placeholder="Nazwa Produktu...")

with col_button_add:
    # Używamy formy do lepszego zarządzania stanem i resetowania pola tekstowego
    with st.container():
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Dodaj do Magazynu", use_container_width=True, type="secondary"):
            add_product(new_product_name)
            # Wymuszenie ponownego uruchomienia skryptu, aby wyczyścić pole wejściowe po dodaniu
            st.session_state.new_product_input = "" 
            st.rerun()


# --- Sekcja Wyświetlania Magazynu ---
st.markdown("---")
st.header("📋 Aktualny Magazyn")

if st.session_state.inventory:
    # Wyświetlenie listy produktów
    inventory_list = st.session_state.inventory
    
    st.dataframe(
        {"Nazwa Produktu": inventory_list}, 
        use_container_width=True,
        hide_index=True
    )
    st.markdown(f"**Liczba unikalnych produktów:** **{len(inventory_list)}**")
else:
    st.info("Magazyn jest obecnie pusty. Dodaj pierwszy produkt powyżej.")


# --- Sekcja Usuwania Produktu ---
st.markdown("---")
st.header("🗑️ Usuwanie Produktu")

if st.session_state.inventory:
    col_remove, col_button_remove = st.columns([3, 1])

    with col_remove:
        # Wybieranie produktu do usunięcia z listy dostępnych
        product_to_remove = st.selectbox(
            "Wybierz produkt do usunięcia:",
            options=st.session_state.inventory,
            key="remove_product_select",
            label_visibility="collapsed"
        )
    
    with col_button_remove:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Usuń Wybrany Produkt", use_container_width=True, type="primary"):
            remove_product(product_to_remove)
            st.rerun() # Wymuszenie odświeżenia, aby zaktualizować listę i SelectBox
else:
    st.warning("Brak produktów w magazynie do usunięcia.")
