import gradio as gr
import requests


BASE_URL = "http://localhost:8000/api"
AGENT_TOKEN = "agent123"
ADMIN_TOKEN = "admin123"


# ---------------------------
# CRM utility functions
# ---------------------------
def _auth_header(role: str):
    if role == "agent":
        return {"Authorization": f"Bearer {AGENT_TOKEN}"}
    if role == "admin":
        return {"Authorization": f"Bearer {ADMIN_TOKEN}"}
    return {}


# ---------------------------
# CRM UI Callbacks
# ---------------------------


def info():
    title = "CRM/Ticketing System"
    welcome = "Welcome to the CRM/Ticketing System!"
    description = "Use the tabs to manage customers, tickets, and notes."
    return {"title": title, "welcome": welcome, "description": description}


def get_customer(customer_id, role):
    try:
        resp = requests.get(
            f"{BASE_URL}/customers/{customer_id}",
            headers=_auth_header(role),
            timeout=5,
        )
        return resp.text
    except Exception as e:
        return f"Error: {e}"


def list_tickets(customer_id):
    try:
        params = {"customer_id": customer_id} if customer_id else {}
        resp = requests.get(f"{BASE_URL}/tickets", params=params, timeout=5)
        return resp.text
    except Exception as e:
        return f"Error: {e}"


def create_ticket(customer_id, subject, description, role):
    try:
        payload = {
            "customer_id": int(customer_id),
            "subject": subject,
            "description": description,
        }
        resp = requests.post(
            f"{BASE_URL}/tickets/",
            json=payload,
            headers=_auth_header(role),
            timeout=5,
        )
        return resp.text
    except Exception as e:
        return f"Error: {e}"


def update_ticket(ticket_id, status, role):
    try:
        payload = {"status": status}
        resp = requests.patch(
            f"{BASE_URL}/tickets/{ticket_id}",
            json=payload,
            headers=_auth_header(role),
            timeout=5,
        )
        return resp.text
    except Exception as e:
        return f"Error: {e}"


def add_note(ticket_id, text, role):
    try:
        resp = requests.post(
            f"{BASE_URL}/notes/{ticket_id}",
            json={"text": text},
            headers=_auth_header(role),
            timeout=5,
        )
        return resp.text
    except Exception as e:
        return f"Error: {e}"


# ---------------------------
# Main UI launcher
# ---------------------------
def launch_ui():
    """
    Script entrypoint used in pyproject.toml.
    Main UI for CRM/Ticketing system.
        - Displays Title and Subtitle.
        - Creates 3 tabs:
            1) Customer Management
            2) Tickets Management
            3) Notes Management
    """

    # CRM/Ticketing System UI Tabs
    with gr.Blocks(title=info().get("title")) as demo:
        # Header
        with gr.Row():
            html_item = f"""
            <center> 
                <h1> {info().get('title')}  </h1>
                <b> {info().get('description')} </b>
            </center>
            """
            gr.HTML(html_item)

        # Tabs
        with gr.Tabs():
            # -------------------
            # Customers Tab
            # -------------------
            with gr.TabItem("Customers"):
                gr.Markdown("Customers API for managing customer data.")
                with gr.Tab("Get Customer"):
                    cid = gr.Number(label="Customer ID", value=1)
                    role = gr.Radio(["agent", "admin"], value="agent", label="Role")
                    fetch_btn = gr.Button("Get Customer")
                    cust_output = gr.Textbox(label="Response")
                    fetch_btn.click(get_customer, inputs=[cid, role], outputs=cust_output)

            # -------------------
            # Tickets Tab
            # -------------------
            with gr.TabItem("Tickets"):
                gr.Markdown("Tickets API for managing customer support tickets.")

                with gr.Tab("List"):
                    gr.Markdown("### List Tickets")
                    list_cid = gr.Number(label="Customer ID (optional)", value=None)
                    list_btn = gr.Button("List")
                    list_out = gr.Textbox(label="Response")
                    list_btn.click(list_tickets, inputs=[list_cid], outputs=list_out)

                with gr.Tab("Create"):
                    gr.Markdown("### Create Ticket")
                    c_cid = gr.Number(label="Customer ID")
                    c_sub = gr.Textbox(label="Subject")
                    c_desc = gr.Textbox(label="Description")
                    c_role = gr.Radio(["agent", "admin"], value="agent", label="Role")
                    c_btn = gr.Button("Create")
                    c_out = gr.Textbox(label="Response")
                    c_btn.click(
                        create_ticket,
                        inputs=[c_cid, c_sub, c_desc, c_role],
                        outputs=c_out,
                    )
                with gr.Tab("Update"):
                    gr.Markdown("### Update Ticket Status")
                    u_tid = gr.Number(label="Ticket ID")
                    u_status = gr.Textbox(label="Status (e.g., in_progress, closed)")
                    u_role = gr.Radio(["agent", "admin"], value="agent", label="Role")
                    u_btn = gr.Button("Update")
                    u_out = gr.Textbox(label="Response")
                    u_btn.click(
                        update_ticket,
                        inputs=[u_tid, u_status, u_role],
                        outputs=u_out,
                    )

            # -------------------
            # Notes Tab
            # -------------------
            with gr.TabItem("Notes"):
                gr.Markdown("Notes API for managing ticket notes.")
                with gr.Tab("Add Note"):
                    n_tid = gr.Number(label="Ticket ID")
                    n_text = gr.Textbox(label="Note text")
                    n_role = gr.Radio(["agent", "admin"], value="admin", label="Role")
                    n_btn = gr.Button("Add Note")
                    n_out = gr.Textbox(label="Response")
                    n_btn.click(add_note, inputs=[n_tid, n_text, n_role], outputs=n_out)

        demo.launch()


def main():
    launch_ui()


if __name__ == "__main__":
    main()
