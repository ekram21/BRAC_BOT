import smtplib
 


def Notify_Seat_Available_By_Mail(Send_Mail_Address):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("pythonbot21@gmail.com", "pythonbot123")
     
    msg = "Seat is available. This is an automated message so please do not reply back to me. BEEP BOOP."
    server.sendmail("pythonbot21@gmail.com", Send_Mail_Address, msg)
    server.quit()



if __name__ == '__main__':
    Notify_Seat_Available_By_Mail('ekram_lol@hotmail.com')