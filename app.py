import streamlit as st
from ask import resolve
from memory import add_memory,load_memory,get_ticket
import chromadb


st.set_page_config(
    page_title = "Triagent",
    layout = "wide"
)

st.title("🤖Triagent")
st.caption("AI-powered Oracle ERP support and troubleshooting")


if "result" not in st.session_state:
    st.session_state.result = None

if "ticket_text" not in st.session_state:
    st.session_state.ticket_text = ""

if "ticket_id" not in st.session_state:
    st.session_state.ticket_id = None

st.sidebar.title("🤖 Triagent")
st.sidebar.caption("ERP Support Assistant")

if st.sidebar.button("➕ New Ticket", use_container_width=True):
    st.session_state.page = "New Ticket"

if st.sidebar.button("🔍 Search Tickets", use_container_width=True):
    st.session_state.page = "Search Tickets"

if "page" not in st.session_state:
    st.session_state.page = "New Ticket"

page = st.session_state.page

if page == "New Ticket":
    st.subheader("Submit the Ticket")

    with st.form("Ticket_form"):

        ticket_text = st.text_area(
            "Describe the issue you are facing",
            placeholder = "Ex:Purchase approval got struck",
            height = 150
            )

        submitted = st.form_submit_button("submit",type = "primary")


    if submitted:

        if not ticket_text.strip():
            st.warning("Please enter a ticket description.")

        else:
            try:
                with st.spinner("AI is analysing your ticket..."):

                    result = resolve(ticket_text)
                    if isinstance(result, dict) and "error" in result:
                        st.session_state.result = None
                        st.session_state.ticket_text = ""
                        st.session_state.ticket_id = None
                        st.warning(result["error"])

                    elif result is not None:
                        ticket_id = add_memory(ticket_text, result)

                        st.session_state.result = result
                        st.session_state.ticket_text = ticket_text
                        st.session_state.ticket_id = ticket_id
                        st.success("Resolution has been generated successfully")
                    else:
                        st.error("Cant able to retrieve the valid diagnosis")
            except Exception as e:
                st.error(f"an error has occured:{e}")
    
    if st.session_state.result is not None:
        result = st.session_state.result 

        st.divider()

        st.header("AI Diagnosis")

        # 1. Original Ticket
        with st.container(border=True):

            st.subheader("Submitted Ticket")

            st.write(st.session_state.ticket_text)

            st.caption(
                f"Ticket ID: {st.session_state.ticket_id}"
            )

        # 2. Ticket Classification
        st.subheader("1. Ticket Classification")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Module", result.Module)

        with col2:
            st.metric("Category", result.Category)

        with col3:
            st.metric("Complexity", result.Complexity.title())

        st.divider()

        # 3. Root Cause Analysis
        st.subheader("2. Root Cause Analysis")

        with st.container(border=True):

            st.write(result.Root_Cause)

        st.divider()

        # 4. Troubleshooting Steps
        st.subheader("3. Recommended Troubleshooting Steps")

        with st.container(border=True):

            for i, step in enumerate(result.Steps, start=1):

                st.markdown(f"**Step {i}**")

                st.write(step)

                if i != len(result.Steps):
                    st.divider()


elif page == "Search Tickets":
    st.subheader("Previous Tickets")

    memory = load_memory()

    if not load_memory():
        st.info("No ticket Exists")

    else:
        st.write(f"Total tickets resolved:{len(memory)}")

        search = st.text_input("Search for tickets",
                               placeholder = "Ex: AP1 or invoice")

        filtered_tickets = []

        for ticket in memory:

            searchable_text = (
                            ticket.get("id","") + " " +
                            ticket.get("ticket","") + " " +
                            ticket.get("Module","") + " " +
                            ticket.get("Category","") 
                            ).lower()
            if search.lower().strip() in  searchable_text:
                filtered_tickets.append(ticket)

        if not filtered_tickets:
            st.info("No tickets found")

        else:

            selected_id = st.selectbox(
                            "Select a ticket",
                            options=[
                                ticket["id"] for ticket in filtered_tickets
                            ],
                            index=None,
                            placeholder="Choose a ticket to view details"
                            )
            if selected_id is not None:
                selected_ticket = get_ticket(selected_id)

                if "error" not in selected_ticket:

                    st.divider()
                    with st.container(border=True):
                        st.markdown(f"### Ticket ID: {selected_ticket['id']}")

                        st.write("**Original Issue:**")
                        st.write(selected_ticket["ticket"])

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        with st.container(border=True):
                            st.caption("MODULE")
                            st.write(selected_ticket["Module"])

                    with col2:
                        with st.container(border=True):
                            st.caption("CATEGORY")
                            st.write(selected_ticket["Category"])

                    with col3:
                        with st.container(border=True):
                            st.caption("COMPLEXITY")
                            st.write(selected_ticket["Complexity"])
                    st.divider()
                    st.subheader("Root Cause:")
                    st.write(selected_ticket["Root Cause"])

                    st.subheader("**Troubleshooting Steps**")

                    for i, step in enumerate(
                        selected_ticket["Steps"], start=1
                        ):
                        st.write(f"**{i}.** {step}")


            