#!/usr/bin/python
import random
import math
import json

from OpenGL.GL import *
from OpenGL.GLUT import *


class Utils():
	'''Utilitiy Class for repeated function calls
	Loads the config for sim from config.json
	'''
	def __init__(self):
		try:
			fp = open('./config.json')
			self.params = json.load(fp)
		except:
			logging.exception("Unable to load the config file")

	@property
	def config(self):
		return self.params

	@staticmethod
	def getRadians(x):
		return math.pi/180.0 * x

	@staticmethod
	def getRandomColor():
		color = [1.0]				#Alpha channel
		for i in range(3):
			color.insert(0,random.random())	
		return  color


# Place holder for all particles in the system
# Made this global, as it needs access across
particleList = []
utils = Utils()
params = utils.config


class Particle(object):
	'''Main Particle class, contains all attributes for a
		particle
	'''
	def __init__(self,x,y,vx,vy,color,size):
		#super(Particle, self).__init__()		
		self.x = x		#Position
		self.y = y		
		self.vx =vx		#velocity components
		self.vy = vy

		self.age= 0		
		self.max_age=params['maxAge']

		self.wind = 0.1
		self.size = size	
		
		self.color=color
		self.is_dead = False

	def update(self,dx=0.05,dy=0.05):
		self.vx += dx* self.wind 
		self.vy += dy*self.wind - params['gravity']/100

		self.vx *= 1- params['dragFactor']/1000
		self.vy *= 1- params['dragFactor']/1000

		self.x += self.vx
		self.y += self.vy
		self.check_particle_age()		

	def draw(self):
		#print "x: %s Y: %s" %(self.x,self.y) 
		glColor4fv(self.color)
		glPushMatrix()
		glTranslatef(self.x,self.y,0)
		glutSolidSphere(self.size,20,20)
		glPopMatrix()
		glutPostRedisplay()

	def check_particle_age(self):		
		self.age +=1 
		self.is_dead = self.age >= self.max_age	

		#Start ageing
		# Achieve a linear color falloff(ramp) based on age.
		self.color[3]= 1.0 - float(self.age)/float(self.max_age)

class ParticleBurst(Particle):	
	def __init__(self,x,y,vx,vy):
		color = params['launchColor']
		size = params['launchSize']		
		Particle.__init__(self,x,y,vx,vy,color,size)
		self.wind=1		

	def explode(self):
		#pick random burst color
		color = Utils.getRandomColor()	
		explodeCount = params['explodeCount']

		for i in range(explodeCount):
			angle = Utils.getRadians(random.randint(0,360))			
			speed = params['explosionSpeed'] * (1 -random.random())
			vx = math.cos(angle)*speed
			vy = -math.sin(angle)*speed
			x  = self.x + vx
			y  = self.y + vy
			# Create Fireworks particles
			obj = Particle(x,y,vx,vy,color,params['particleSize'])			
			particleList.append(obj)

	# Override parent method for Exploder particle
	def check_particle_age(self):
		
		if self.vy <0:
			self.age += 1

		# Tweaking explode time
		temp = int ( 100*  random.random()) + params['explosionVariation']
		
		if self.age > temp:
			self.is_dead = True			
			self.explode()

class ParticleSystem():
	'''Container class for the Simulation.
	Takes care to add Exploders at a given interval
	'''
	def __init__(self):		
		self.x = params['initPosX']
		self.y = params['initPosY']
		self.timer = 0
		self.addExploder()
		#self.explode()

	def addExploder(self):
		speed = params['explosionSpeed']
		speed *= (1 - random.uniform(0,params['explosionVariation'])/100)
		angle = 270*3.14/180 + round(random.uniform(-0.5,0.5),2)
		vx = speed * math.cos(angle) 
		vy = -speed * math.sin(angle)
		
		f = ParticleBurst(30,10,vx,vy )			
		particleList.append(f)

	def update(self):
		# Clock to launch fireworks,
		interval = params['launchIterval']
		self.timer += 1

		if self.timer % interval == 0 or self.timer < 2:		
			self.addExploder()
		
		for i in range(len(particleList)-1,0,-1):
			p = particleList[i]
			x = params['windX']
			y = params['windY']						
			p.update(x,y)
			p.check_particle_age()			
			if p.is_dead:					
				p.color = [0.0,0.0,0.0,0.0]				
				particleList.pop(i)				
			else:
				p.draw()