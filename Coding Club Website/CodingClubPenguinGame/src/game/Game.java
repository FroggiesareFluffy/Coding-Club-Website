package game;

import java.applet.Applet;
import java.awt.Graphics;
import java.awt.Color;

public class Game extends Applet {
	private static final long serialVersionUID = 1L;
	
	public void paint(Graphics g){
		g.drawString("Northglenn HS Coding Club",25,50);
	}
	
	public void init(){
		setBackground(new Color(255,0,0));
		setForeground(new Color(0,0,255));
		setSize(600,200);
	}
}
