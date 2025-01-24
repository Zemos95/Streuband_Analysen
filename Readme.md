## Erarbeitung einer Streubanderkennung

Gleitender Mittelwert:

Der gleitende Mittelwert wird mit einer Fenstergröße von 1 Sekunde (50 Werte) berechnet.
Dies glättet die Signaldaten und dient als Referenz für das Toleranzband.
Dynamisches Toleranzband:

Die oberen und unteren Grenzen des Toleranzbands werden basierend auf dem gleitenden Mittelwert definiert:
Obere Grenze
=
Mittelwert
+
2
 
𝜇
m/m
Obere Grenze=Mittelwert+2μm/m
Untere Grenze
=
Mittelwert
−
2
 
𝜇
m/m
Untere Grenze=Mittelwert−2μm/m
Ausreißer-Detektion:

Punkte, die außerhalb der dynamischen Grenzen liegen, werden als Ausreißer markiert und rot hervorgehoben.
Visualisierung:

Das unbelastete und belastete Signal werden in separaten Plots dargestellt.
Der gleitende Mittelwert und das Toleranzband sind eingezeichnet.
Punkte außerhalb des Toleranzbands sind als rote Punkte hervorgehoben.