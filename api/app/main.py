from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app import db

app = FastAPI(title="desk-api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class TicketIn(BaseModel):
    title: str
    body: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/tickets", status_code=201)
def create_ticket(ticket: TicketIn):
    """Insert a ticket (status=new) and an ack job (status=pending) in one transaction."""
    with db.connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO tickets (title, body)
                VALUES (%s, %s)
                RETURNING id, title, body, status, acknowledgement, created_at
                """,
                (ticket.title, ticket.body),
            )
            created = cur.fetchone()
            cur.execute(
                "INSERT INTO jobs (ticket_id, type) VALUES (%s, 'ack')",
                (created["id"],),
            )
        conn.commit()
    return created


@app.get("/tickets")
def list_tickets():
    """Return tickets, newest first."""
    with db.connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, title, body, status, acknowledgement, created_at
                FROM tickets
                ORDER BY created_at DESC
                """
            )
            return cur.fetchall()


@app.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: int):
    """Return one ticket, or 404."""
    with db.connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, title, body, status, acknowledgement, created_at
                FROM tickets
                WHERE id = %s
                """,
                (ticket_id,),
            )
            ticket = cur.fetchone()
    if ticket is None:
        raise HTTPException(status_code=404, detail="ticket not found")
    return ticket
