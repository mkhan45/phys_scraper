import fitz
import pytesseract
import asyncio
import os
import multiprocessing
from multiprocessing import Process

def scrape_pdf(pdf_path):
    print(f"Scraping {pdf_path}...")
    pdf = fitz.open(pdf_path)
    txt = ""
    for page in pdf:
        pixmap = page.get_pixmap(dpi=250)
        img = pixmap.tobytes()
        fname = f"{pdf_path}-page-{page.number}.png"
        with open(fname, "wb") as f:
            f.write(img)
        txt += pytesseract.image_to_string(fname)
        os.remove(fname)

    q1_delim = "1. Please paste the completed code for apply_spring force below"
    q2_delim = "2. Please paste the completed code for calculate_kinetic_energy below"
    q3_delim = "3. Please paste the completed code for calculate_potential_energy below"
    q4_delim = "4. When is the potential energy maximized, and when is the kinetic energy maximized?"
    q5_delim = "How does increasing/decreasing the DAMPING_FACTOR\nand dt affect the graph?"
    end_delim = "Save this document as PDF and upload it in the link provided on Brightspace."

    q1 = txt.split(q1_delim)[1].split(q2_delim)[0]
    q2 = txt.split(q2_delim)[1].split(q3_delim)[0]
    q3 = txt.split(q3_delim)[1].split(q4_delim)[0]
    q4 = txt.split(q4_delim)[1].split(q5_delim)[0]
    q5 = txt.split(q5_delim)[1].split(end_delim)[0]

    print(f"Finished scraping {pdf_path}")
    return q1, q2, q3, q4, q5

if __name__ == "__main__":
    # find all pdfs in current directory
    pdfs = [f for f in os.listdir() if f.endswith(".pdf")]

    if not os.path.exists("results"):
        os.makedirs("results")
    def full_scrape(pdf):
        (q1, q2, q3, q4, q5) = scrape_pdf(pdf)
        with open(f"results/result-{pdf}.txt", "w") as f:
            f.write(f"Question 1:\n{q1}\n\n")
            f.write(f"Question 2:\n{q2}\n\n")
            f.write(f"Question 3:\n{q3}\n\n")
            f.write(f"Question 4:\n{q4}\n\n")
            f.write(f"Question 5:\n{q5}\n\n")

    processes = [Process(target=full_scrape, args=(pdf,)) for pdf in pdfs]
    for p in processes: p.start()
    for p in processes: p.join()
