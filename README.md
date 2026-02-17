# 🌙 Ramadan Spiritual Jar (Digital Name Picker) 

This project is a digital transformation of the traditional "Ramadan Jar." Instead of physical paper slips, this app manages a list of participants who commented on the Ramadan post. Every day at Iftar, a name (or multiple names) is drawn for a special prayer (Duaa).

## 🕌 The Ramadan Initiative
> "From now until the first day of Ramadan, I will collect the names of everyone who comments on the post. Every day during Ramadan at Iftar time, I will pull a name and offer a heartfelt prayer (Duaa) for them. If the number of participants is large, I will pull two or three names daily."
>
> **رمضان كريم**
## ✨ Features
- **Persistent Storage:** Uses `data.json` to ensure names gathered before Ramadan stay safe until the month begins.
- **Daily Draw:** Choose to pick 1, 2, or 3 names depending on the total count.
- **Duaa History:** Keeps track of everyone who has been prayed for throughout the month.
- **Automatic Removal:** Ensures every participant gets their turn by removing them from the "Jar" once picked.

## 🚀 Setup & Usage
1. **Install Requirements:** ```bash
   pip install streamlit
