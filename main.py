import math, random
import direct.directbase.DirectStart
from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
from direct.task.Task import Task

prime = render.attachNewNode('prime')
#Global Collision setup
base.cTrav = CollisionTraverser('Collision Detection')
Pusher = CollisionHandlerPusher() #this handler will generate a a panda event for each collision that can be accepted by the various classes in addition to providing simple real world collisions.
Pusher.addInPattern('%fn') #the format of the actual event string.  Just provide the name of the "from" node

collisionMASK = BitMask32.bit(1)

class Guide2D:

	def __init__(self, pos = None, hpr = None,):
		self.guide = prime.attachNewNode('Guide'+str(self.name))  #This node will be the moving and turning node. Pos and Hpr should be set to self.guide
		self.guide.setPos(pos)
		self.guide.setHpr(hpr)
		self.pointer = NodePath('pointer'+str(self.name))
		self.pointer.reparentTo(prime)
		self.speed = self.maxspeed  #some functions require speeds other than the max speed. This speed is the actual speed of the unit.
	def Guidestep(self,dt):
		if self.pointer.isEmpty(): return
		if self.guide.isEmpty():return
		self.pointer.setPos(self.guide.getPos())
		for methods in self.behavior:
			methodname = '_steerFor' + methods
			method = getattr(self,methodname)
			method(dt)		
		self.guide.setFluidPos(self.guide,Vec3(0,1*dt*self.speed,0))
	
	def _steerForSeek(self,dt):
		self.speed = self.maxspeed
		if self.target is None: return
		if self.target.isEmpty() == False:
			
			self.pointer.lookAt(self.target)
			PH = self.pointer.getH()
			GH = self.guide.getH()
			H = None
			add = 0
			if GH < 0: add = 1
			if PH < 0: add = add + 1
			if add == 1: 
				#Different sides of the divide
				a = abs(GH) + abs(PH)
			else:
				#Same side of the divide
				a = abs(GH - PH)
			b = 360 - a
			if b < 180: Switch = -1
			else: Switch = 1
			
			if PH > GH: 
				if abs(PH-GH) > self.rotation * dt:	H = GH+self.rotation*dt*Switch #This will hopefully prevent jitter when approximating the pointer position.
				else: H = GH + self.rotation/5 * dt * Switch
				
			if PH < GH: 
				if abs(PH-GH) > self.rotation * dt:	H = GH-self.rotation*dt*Switch #This will hopefully prevent jitter when approximating the pointer position.
				else: H = GH - self.rotation/5 * dt * Switch
							
			if H is not None: 
				if H < -180: H = 179
				if H > 180 : H = -179
				self.guide.setH(H)
	def _steerForFlee(self,dt):
		self.speed = self.maxspeed
		if self.target is None: return
		if self.target.isEmpty() == False:
			self.pointer.lookAt(self.target)
			PH = self.pointer.getH()
			GH = self.guide.getH()
			H = None
			add = 0
			if GH < 0: add = 1
			if PH < 0: add = add + 1
			if add == 1: 
				#Different sides of the divide
				a = abs(GH) + abs(PH)
			else:
				#Same side of the divide
				a = abs(GH - PH)
			b = 360 - a
			if b < 180: Switch = -1
			else: Switch = 1
			
			if PH > GH: 
				H = GH - self.rotation*dt*Switch*5
			
			if PH < GH: 
				H = GH + self.rotation*dt*Switch*5
				
			if H is not None: 
				if H < -180: H = 179
				if H > 180 : H = -179
				self.guide.setH(H)
				
			
	def _steerForWander(self,dt):
		self.speed = self.maxspeed/2
		GH = self.guide.getH()
		PH = self.pointer.getH()
		if abs(GH-PH) < 10: self.pointer.setH(random.random()*360-180)
		H = None
			
		add = 0
		if GH < 0: add = 1
		if PH < 0: add = add + 1
		if add == 1: 
			#Different sides of the divide
			a = abs(GH) + abs(PH)
		else:
			#Same side of the divide
			a = abs(GH - PH)
		b = 360 - a
		if b < 180: Switch = -1
		else: Switch = 1
		
		if PH > GH: 
			
			if abs(PH-GH) > self.rotation * dt:	H = GH+self.rotation/2*dt*Switch 
			else: H = GH + self.rotation/5 * dt * Switch
			
		if PH < GH: 
			if abs(PH-GH) > self.rotation * dt:	H = GH-self.rotation/2*dt*Switch 
			else: H = GH - self.rotation/5 * dt * Switch
			
		if H is not None: 
			if H < -180: H = 179
			if H > 180 : H = -179
			self.guide.setH(H)
		
	def _steerForStop(self,dt):
		self.speed = 0

class Player(Guide2D, DirectObject):
	def __init__(self, world, name):
		
		self.maxspeed = 10
		self.rotation = 90
		self.behavior = ['Wander']
		self.world = world
		
		X = random.random()* 50 - 25
		Y = random.random()* 50 - 25
		H = random.random()*360 - 180 
		pos = Vec3(X,Y,0)
		hpr = Vec3(H,0,0)
		
		self.center = prime.attachNewNode('center'+str(X))
		self.model = loader.loadModel("models/robot.egg.pz")
		self.model.setHpr(90,0,0)
		self.model.reparentTo(self.center)
		
		self.center.reparentTo(prime)
		self.center.setPos(X,Y,0)
		self.name = name
		Guide2D.__init__(self,pos,hpr) #the guide2d object handles movement. We need to give it the starting position and the orientation. 
		#Set up a task for each player. Set up some starting values for timing. Set the player as "not It" as default. 
		self.stepTask = taskMgr.add(self.step, "UnitStepLoop")
		self.stepTask.last = 0
		self.onefourth = 0
		self.Im_not_it()
		self.timer = 2
		
		#Collision stuff
		self.center.setTag("Name",self.name)
		self.colsphere = CollisionSphere(0,0,0,1) 
		self.csnodepath = self.center.attachNewNode(CollisionNode('cnode'))
		self.csnodepath.node().addSolid(self.colsphere)
		self.csnodepath.node().setCollideMask(collisionMASK)
		
		Pusher.addCollider(self.csnodepath, self.guide) 
		base.cTrav.addCollider(self.csnodepath, Pusher) 
		
		self.csnodepath.setTag("Name",self.name)
		self.csnodepath.setName(self.name)
		
		self.accept(self.name, self.Collision)
		
		# default stuff
		self.it = False
		self.isLeader = False
		self.myLeader = None
		
	def Im_it(self):
		self.it = True
		self.center.setColor(1,0,0,1)
		self.maxspeed = 11
		self.world.whoisit = self
		self.ingame = True
	def Im_it2(self):
		self.it = True
		self.center.setColor(1,0,0,1)
		self.maxspeed = 11
		self.world.whoisit2 = self
		self.ingame = True
	def Im_not_it(self):
		self.it = False
		self.iAmAleader = False
		self.center.setColor(0,0,1,1)
		self.maxspeed = 10
		self.ingame = True
	def iAmALeader(self):
		self.isLeader = True
		self.it = False
		self.center.setColor(1,0,5,1)
		self.maxspeed = 10
		self.ingame = True
	def setLeader(self,leader):
		self.isLeader = False
		self.myLeader = leader
	def Im_out(self): #A temporary state for when a player just gets done tagging another player. 
		self.it = False
		self.isLeader = False
		self.center.setColor(0,1,0,1)
		self.maxspeed = 10
		self.ingame = False
		self.timer = 0
	def step(self,task):
		dt = task.time - task.last  #obtains the time since that last frame.
		task.last = task.time
		self.timer = self.timer + dt
		if self.timer >= 1 and self.ingame == False: 
			self.Im_not_it() #put players that were just it back into play after 1 sec. 
		self.Guidestep(dt)
		self.center.setPos(self.guide.getPos())
		self.center.setHpr(self.guide.getHpr())
				
		self.onefourth = self.onefourth + dt # Every 1/4 second update AI
		if self.onefourth > .5: 
			self.onefourth = 0
			self.reset()
		return Task.cont    #finished, the loop goes back to the start.
	def Collision(self,entry):
		intonode = entry.getIntoNodePath()
		name = intonode.getTag("Name")
		if name is not None:
			if not self.it and not self.isLeader:
				if self.ingame:
					if name == self.world.whoisit.name:
						self.world.whoisit.Im_out()
						self.Im_it()
					elif name == self.world.whoisit2.name:
						self.world.whoisit2.Im_out()
						self.Im_it2()
					
	def reset(self):  #This is the key AI routine regarding the rules of Tag. 
		if self.it:
			distance = 100
			temporaryTarget = None
			for player in self.world.players:
				if player.ingame:
					if player != self.world.whoisit and player != self.world.whoisit2 and not player.isLeader:
						if self.center.getDistance(player.center) < distance:
							temporaryTarget = player
							distance = self.center.getDistance(player.center)
			self.Target = temporaryTarget
			self.target = temporaryTarget.center
			self.behavior = ['Seek']
		elif self.myLeader is not None:
			self.Target = self.myLeader
			self.target = self.myLeader.center
			self.behavior = ['Seek']
		elif self.isLeader:
			if self.center.getDistance(self.world.whoisit.center) <= 30:
				self.target = self.world.whoisit.center
				self.behavior = ['Flee']
			elif self.center.getDistance(self.world.whoisit2.center) <= 30:
				self.target = self.world.whoisit2.center
				self.behavior = ['Flee']
			else:
				self.behavior = ['Wander']
		elif self.center.getDistance(self.world.whoisit.center) <= 10:
			self.target = self.world.whoisit.center
			self.behavior = ['Flee']
		elif self.center.getDistance(self.world.whoisit2.center) <= 10:
			self.target = self.world.whoisit2.center
			self.behavior = ['Flee']
		else:
			self.behavior = ['Wander']	
				
class World:
	def __init__(self):
		base.setBackgroundColor(1, 1, 1)    #Set the background to white
		self.setupLights()
		base.camera.setPos(0,-100,100)
		base.camera.setHpr(0,-45,0)
		base.disableMouse()
	
		
		#Load up the model for the playing field. 
		field = loader.loadModel("models/field.egg")
		field.reparentTo(prime)
		field.setPosHprScale(0,0,-.5,0,-90,0,83,83,83)
					
		self.players = []
		for i in range(20):
			p = Player(self,str(i))	#create a new player- pass the player the this world class for reference.
			self.players.append(p)			
		
		self.players[0].Im_it()  #just assign the number 10 player to be IT to start off the game. 
		self.players[1].Im_it2()  #just assign the number 15 player to be IT to start off the game. 
		
		self.players[5].iAmALeader() 
		self.players[6].setLeader(self.players[5]) 
		self.players[7].setLeader(self.players[5]) 
		self.players[8].setLeader(self.players[5])
		
		self.players[10].iAmALeader() 
		self.players[11].setLeader(self.players[10]) 
		self.players[12].setLeader(self.players[10]) 
		self.players[13].setLeader(self.players[10])
		
		self.setupPlayField()

	def setupLights(self):
		prime.setLightOff() #clears the field so that only these lights are ever in play.
		# Setup ambient and directional lights.
		self.alight = AmbientLight('alight')
		self.alight.setColor(VBase4(0.35, 0.35, 0.35, 1)) #formerly .15
		self.alnp = prime.attachNewNode(self.alight)
		prime.setLight(self.alnp)

		self.dlight = DirectionalLight('dlight')
		self.dlight.setColor(VBase4(0.9, 0.9, 0.9, 1))
		self.dlnp = prime.attachNewNode(self.dlight)
		self.dlnp.setHpr(45, -15, 0)
		prime.setLight(self.dlnp)	
	def setupPlayField(self): #this sets the outer bounds of the playfield as an inverse collision sphere. 
		inv = CollisionInvSphere(0, 0, 0, 40)
		cnodePath = prime.attachNewNode(CollisionNode('inv'))
		cnodePath.node().addSolid(inv)
		
		
w = World()
run()