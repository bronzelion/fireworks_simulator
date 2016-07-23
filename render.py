#!/usr/bin/python
#Using PyOpenGL,OpenGLContext for Rendering.

import logging
from fireworks import *
from OpenGLContext import testingcontext 

BaseContext = testingcontext.getInteractive()
BaseContext.APPLICATION_NAME="Fireworks"
logging.basicConfig()


class TestContext(BaseContext):	
	'''	
	OpenGL Rendering Setup
	'''	
	def OnInit(self):	
		# Initialize Fireworks
		self.fireworks = ParticleSystem()		
		
	def Render( self, mode):
		glOrtho(0,150,0,150,0,100)
		glDisable( GL_CULL_FACE )
		glDisable(GL_LIGHTING)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
		glEnable(GL_BLEND)

		#Do the magic!
		self.fireworks.update()
		
if __name__ == "__main__": 
	TestContext.ContextMainLoop() 