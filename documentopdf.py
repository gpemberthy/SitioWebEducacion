from reportlab.pdfgen import canvas

def generate_pdf():

    # Create the canvas
    pdf_canvas = canvas.Canvas("example2.pdf", pagesize=(400,300))
    
    #xlist = [10, 60, 110, 160]
    #ylist = [10, 60, 110, 160]
    #pdf_canvas.grid(xlist, ylist)
    #roundRect(x, y, width, height, radius, stroke=1, fill=0)
    # Cuadrante superior donde esta el nombre del conjunto
    pdf_canvas.setFillColorRGB(211/255, 211/255, 211/255) 
    pdf_canvas.roundRect(10, 240, 380, 50, 4, stroke=1, fill=1)
    
    #Cuadrante central
    pdf_canvas.setFillColorRGB(210/255, 255/255, 210/255) 
    pdf_canvas.roundRect(10, 10, 380, 177, 4, stroke=1, fill=1)
    
    pdf_canvas.setFillColorRGB(210/255, 210/255, 225/255)
    pdf_canvas.roundRect(10, 192, 380, 45, 4, stroke=1, fill=1)

    #Cuandrante del numero del comprobante
    pdf_canvas.setFillColorRGB(255/255, 255/255, 255/255) 
    pdf_canvas.roundRect(255, 195, 125, 40, 4, stroke=1, fill=1)

    pdf_canvas.setDash(4,3)
    pdf_canvas.line(100,158,260,158)
    pdf_canvas.line(100,122,260,122)
    """
    pdf_canvas.line(10,240,380,240)
    pdf_canvas.line(10,10,380,10)
    pdf_canvas.line(10,10,380,10)
    #lineas verticales
    pdf_canvas.setLineWidth(5)
    pdf_canvas.line(10,290,10,10)
    pdf_canvas.line(380,290,380,10)
    """
    pdf_canvas.setFillColorRGB(0,0,0)
    pdf_canvas.setFont("Helvetica-Bold", 14)
    pdf_canvas.drawString(60, 265, "DUQUE OCHOA PROPIEDAD HORIZONTAL")
    pdf_canvas.setFont("Helvetica", 8)
    pdf_canvas.drawString(160, 255, "Nit: 900.740.113-3")
    pdf_canvas.drawString(150, 245, "Cra 8a # 20a-138 / 14s8")
    
    #pdf_canvas.setFont("Courier", 10)
    pdf_canvas.setFont("Helvetica-Bold", 10)
    pdf_canvas.drawString(270, 218, "SOPORTE DE PAGO")
    pdf_canvas.setFillColorRGB(255,0,0)
    pdf_canvas.setFont("Helvetica-Bold", 14)
    pdf_canvas.drawString(310, 200, "560")
    
    pdf_canvas.setFont("Times-Bold", 12)
    pdf_canvas.setFillColorRGB(0, 0, 0)
    pdf_canvas.drawString(45, 220   , "Fecha:     ")
    pdf_canvas.drawString(45, 200, "Ciudad:     ")
    pdf_canvas.drawString(280, 160, "Casa No:")
    pdf_canvas.setFont("Times-Roman", 14)
    pdf_canvas.drawString(25, 160, "Pagado Por: ")
    pdf_canvas.setFont("Times-Roman", 12)
    pdf_canvas.drawString(25, 125, "La Suma de:")
    
    pdf_canvas.drawString(25, 100, "Efectivo                     Consignacion                     Transferencia")
    
    pdf_canvas.setFont("Helvetica-Bold", 10)
    pdf_canvas.drawString(25, 70, "Transacción No:")
    pdf_canvas.drawString(25, 50, "Entidad Financiera:")
    pdf_canvas.setFont("Courier-Oblique", 7.5)
    pdf_canvas.drawString(25, 30, "Numero de cuenta de Ahorros Banco Davivienda:  462500020963")
    pdf_canvas.drawString(25, 20, "Este soporte es su comprobante del pago realizado a la administración")
    
    #llenado de la informacion
    pdf_canvas.setFont("Courier-Bold", 10)
    pdf_canvas.drawString(95, 220, "05/09/2023")
    pdf_canvas.drawString(95, 200, "Cajica")
    pdf_canvas.setFont("Courier-Bold", 14)
    pdf_canvas.drawString(335, 160, "14")
    pdf_canvas.setFont("Courier-Bold", 10)
    pdf_canvas.drawString(105, 160, "Luis Fernando Gonzalez")
    pdf_canvas.setFont("Courier-Bold", 14)
    pdf_canvas.drawString(135, 125, "100.000")
    pdf_canvas.drawString(130, 70, "xxxxxxxx")
    pdf_canvas.drawString(130, 50, "xxxxxxxx")
    # Save the PDF
    pdf_canvas.save()

def generate_pdf2():
    # Create the canvas
    pdf_canvas = canvas.Canvas("Recibo.pdf", pagesize=(400,350))
    
    #xlist = [10, 60, 110, 160]
    #ylist = [10, 60, 110, 160]
    #pdf_canvas.grid(xlist, ylist)
    #roundRect(x, y, width, height, radius, stroke=1, fill=0)
    
    # Cuadrante superior donde esta el nombre del conjunto
    pdf_canvas.setFillColorRGB(211/255, 211/255, 211/255) 
    pdf_canvas.roundRect(10, 290, 380, 50, 4, stroke=1, fill=1)
    
    #Cuadrante central
    pdf_canvas.setFillColorRGB(210/255, 255/255, 210/255) 
    pdf_canvas.roundRect(10, 10, 380, 228, 4, stroke=1, fill=1)
    
    #Segundo cuadrante
    pdf_canvas.setFillColorRGB(210/255, 210/255, 225/255)
    pdf_canvas.roundRect(10, 242, 380, 45, 4, stroke=1, fill=1)

    #Cuandrante del numero del comprobante
    pdf_canvas.setFillColorRGB(255/255, 255/255, 255/255) 
    pdf_canvas.roundRect(255, 245, 125, 40, 4, stroke=1, fill=1)

    pdf_canvas.line(10,216,390,216)
    pdf_canvas.setDash(4,3)
    pdf_canvas.line(100,158,260,158)

    """
    pdf_canvas.line(10,240,380,240)
    pdf_canvas.line(10,10,380,10)
    pdf_canvas.line(10,10,380,10)
    #lineas verticales
    pdf_canvas.setLineWidth(5)
    pdf_canvas.line(10,290,10,10)
    pdf_canvas.line(380,290,380,10)
    """
    pdf_canvas.setFillColorRGB(0,0,0)
    pdf_canvas.setFont("Helvetica-Bold", 14)
    pdf_canvas.drawString(60, 315, "DUQUE OCHOA PROPIEDAD HORIZONTAL")
    pdf_canvas.setFont("Helvetica", 8)
    pdf_canvas.drawString(160, 305, "Nit: 900.740.113-3")
    pdf_canvas.drawString(150, 295, "Cra 8a # 20a-138 / 14s8")
    
    #pdf_canvas.setFont("Courier", 10)
    pdf_canvas.setFont("Helvetica-Bold", 10)
    pdf_canvas.drawString(270, 268, "RECIBO DE PAGO")
    pdf_canvas.setFillColorRGB(255,0,0)
    pdf_canvas.setFont("Helvetica-Bold", 14)
    pdf_canvas.drawString(310, 250, "560")
    
    pdf_canvas.setFont("Times-Bold", 10)
    pdf_canvas.setFillColorRGB(0, 0, 0)
    pdf_canvas.drawString(25, 270   , "Fecha:     ")
    pdf_canvas.drawString(145, 270, "Ciudad:     ")
    pdf_canvas.setFont("Times-Bold", 12)
    pdf_canvas.drawString(30, 220, "  Concepto ")
    pdf_canvas.drawString(250, 220, "Fecha             Valor")
    pdf_canvas.drawString(50, 250, "Casa No:")
   
    pdf_canvas.setFont("Courier-Oblique", 7.5)
    pdf_canvas.drawString(25, 30, "Numero de cuenta de Ahorros Banco Davivienda:  462500020963")
    pdf_canvas.drawString(25, 20, "Este es su comprobante del pago realizado a la administración")
    
    #llenado de la informacion
    pdf_canvas.setFont("Courier-Bold", 10)
    pdf_canvas.drawString(60, 270, "05/09/2023")
    pdf_canvas.drawString(195, 270, "Cajica")
    pdf_canvas.setFont("Courier-Bold", 14)
    pdf_canvas.drawString(200, 250, "14")
    
    pdf_canvas.setFont("Courier-Bold", 10)
    pdf_canvas.drawString(25, 200, "Pago Recibido")
    pdf_canvas.drawString(240, 200, "05/09/2023")
    pdf_canvas.drawString(320, 200, "100.000")
    pdf_canvas.drawString(25, 180, "Cuota administración Mes Octubre")
    pdf_canvas.drawString(240, 180, "01/10/2023")
    pdf_canvas.drawString(320, 180, "100.000")

    # Save the PDF
    pdf_canvas.save()

def generate_pdf_estado_cuenta():
        # Create the canvas
    pdf_canvas = canvas.Canvas("Estado_Cuenta.pdf", pagesize=(500,400))
    
    #xlist = [10, 60, 110, 160]
    #ylist = [10, 60, 110, 160]
    #pdf_canvas.grid(xlist, ylist)
    #roundRect(x, y, width, height, radius, stroke=1, fill=0)
    
    # Cuadrante superior donde esta el nombre del conjunto
    pdf_canvas.setFillColorRGB(211/255, 211/255, 211/255) 
    pdf_canvas.roundRect(10, 340, 480, 50, 4, stroke=1, fill=1)

    #Segundo cuadrante
    pdf_canvas.setFillColorRGB(210/255, 210/255, 225/255)
    pdf_canvas.roundRect(10, 291, 480, 45, 4, stroke=1, fill=1)

    #Cuadrante central
    pdf_canvas.setFillColorRGB(210/255, 255/255, 210/255) 
    pdf_canvas.roundRect(10, 10, 480, 270, 4, stroke=1, fill=1)
    
    #Cuandrante del numero del comprobante
    pdf_canvas.setFillColorRGB(255/255, 255/255, 255/255) 
    pdf_canvas.roundRect(335, 294, 125, 40, 4, stroke=1, fill=1)

    pdf_canvas.line(10,216,390,216)
    pdf_canvas.setDash(4,3)
    pdf_canvas.line(100,158,260,158)

    pdf_canvas.setFillColorRGB(0,0,0)
    pdf_canvas.setFont("Helvetica-Bold", 14)
    pdf_canvas.drawString(100, 370, "DUQUE OCHOA PROPIEDAD HORIZONTAL")
    pdf_canvas.setFont("Helvetica", 8)
    pdf_canvas.drawString(200, 360, "Nit: 900.740.113-3")
    pdf_canvas.drawString(190, 350, "Cra 8a # 20a-138 / 14s8")
    
    #pdf_canvas.setFont("Courier", 10)
    pdf_canvas.setFont("Helvetica-Bold", 10)
    pdf_canvas.drawString(350, 320, "Estado de la Cuenta")
    pdf_canvas.setFillColorRGB(255,0,0)
    pdf_canvas.setFont("Helvetica-Bold", 14)
    pdf_canvas.drawString(370, 302, "MORA")
    
    pdf_canvas.setFont("Times-Bold", 10)
    pdf_canvas.setFillColorRGB(0, 0, 0)
    pdf_canvas.drawString(25, 317   , "Fecha:     ")
    pdf_canvas.drawString(165, 317, "Ciudad:     ")
    pdf_canvas.setFont("Times-Bold", 12)
    pdf_canvas.drawString(30, 260, "Valor cuota:")
    pdf_canvas.drawString(250, 220, "Fecha             Valor")
    pdf_canvas.drawString(70, 300, "Casa No:")
   
    pdf_canvas.setFont("Courier-Oblique", 7.5)
    pdf_canvas.drawString(25, 30, "Numero de cuenta de Ahorros Banco Davivienda:  462500020963")
    pdf_canvas.drawString(25, 20, "Este documento es de caracter informativo. Cualquier inquietud por favor remitirla a la administración")
    
    #llenado de la informacion
    pdf_canvas.setFont("Courier-Bold", 10)
    pdf_canvas.drawString(60, 317, "05/09/2023")
    pdf_canvas.drawString(215, 317, "Cajica")
    pdf_canvas.setFont("Courier-Bold", 14)
    pdf_canvas.drawString(160, 300, "14")
    
    pdf_canvas.setFont("Courier-Bold", 10)
    pdf_canvas.drawString(25, 200, "Pago Recibido")
    pdf_canvas.drawString(240, 200, "05/09/2023")
    pdf_canvas.drawString(320, 200, "100.000")
    pdf_canvas.drawString(25, 180, "Cuota administración Mes Octubre")
    pdf_canvas.drawString(240, 180, "01/10/2023")
    pdf_canvas.drawString(320, 180, "100.000")

    # Save the PDF
    pdf_canvas.save()

def generate_pdf_paz_ySalvo():
        # Create the canvas
    pdf_canvas = canvas.Canvas("PazySalvo.pdf", pagesize="Letter")
    
    pdf_canvas.setFillColorRGB(0,0,0)
    pdf_canvas.setFont("Times-Bold", 18.5)
    pdf_canvas.drawString(230, 640, "PAZ Y SALVO")
    pdf_canvas.setFont("Helvetica", 14)
    pdf_canvas.drawString(70, 560, "La Administracion del Conjunto  Copropiedad Duque Ochoa Propiedad")
    pdf_canvas.drawString(70, 535, "Horizontal  identificada  con  Nit:  900.740.113-3,  se  permite  certificar ")
    pdf_canvas.drawString(70, 510, "que el señor: ")
    pdf_canvas.drawString(170, 510, "XXX XXXXXXX XXXXX")
    pdf_canvas.drawString(388, 510, "identificado con CC: ")
    pdf_canvas.drawString(70, 485, "XXX XXXXXXX XX")
    pdf_canvas.drawString(203, 485, "propietario de la casa numero XX, se encuentra a ")
    pdf_canvas.drawString(70, 460, "Paz y  Salvo  por  todo  concepto  en  lo  que  se refiere  al pago  de  la")
    pdf_canvas.drawString(70, 435, "administración  del  Conjunto  ubicado  en  la  Cra  8a # 20a - 148 / 138")
    pdf_canvas.drawString(70, 410, "del  Barrio  Capellania  /  Cajica  -  Cundinamarca, hasta  el  mes  de")
    pdf_canvas.drawString(70, 385, " XXXXXXX del presente año")
    pdf_canvas.drawString(70, 335, "El presente paz y salvo  se  expide a solicitud  del  interesado  a  los  xx ")
    pdf_canvas.drawString(70, 310, "del mes de XXXXXXX del año 2023")
    pdf_canvas.drawString(70, 270, "Cordialmente,")

    pdf_canvas.drawString(70, 140, "Administración,")
    pdf_canvas.drawString(70, 120, "Copropiedad Duque Ochoa Propiedad Horizontal")
    pdf_canvas.drawString(70, 100, "Nit: 900.740.113-3")

    # Save the PDF
    pdf_canvas.save()

generate_pdf_estado_cuenta()