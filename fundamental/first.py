ujian = 90
absen = 90

def nilai (ujian, absen):
  if ujian >= 90 and absen >= 90:
    return "A"
  elif ujian >= 80 and absen >= 80:
    return "B"
  elif ujian >= 70 and absen >= 70:
    return "C"
  elif ujian >= 60 and absen >= 60:
    return "D"
  else:
    return "E"
  
grade = nilai (90, 90)

match grade:
  case "A":
    print("Nilai kamu A — Hebat banget! 🎉")
  case "B":
    print("Nilai kamu B — Bagus, tetap semangat 💪")
  case "C":
    print("Nilai kamu C — Perlu sedikit peningkatan 📚")
  case "D":
    print("Nilai kamu D — Belajar lebih giat ya 🔥")
  case "E":
    print("Nilai kamu E — Jangan menyerah! Kamu pasti bisa 🙌")

nilai(90, 90)