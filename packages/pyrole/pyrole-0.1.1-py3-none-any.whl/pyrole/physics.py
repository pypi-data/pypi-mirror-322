

G=9.8

def gravity_acceleration(g=None):
    global G
    if g is None:
        return G
    G=g
    return G


def init_role(role):
    role.physical_attributes={
        'elasticity':0.75,#弹性，若大于1，每次弹起将会获得比之前更大的反弹力(这并不科学，所以尽量使这个值小于1)。
        'exercise':[0,0],#运动的向量，是一个长度为2的列表。
        'gravityAngle':-90,#重力的方向
        'Be affected by gravity':True,#角色是否受重力影响，默认为是。
        'Physical boundary':'nswe',#物理边界，碰到哪些边缘地方会反弹，上北下南左西右东。
        'Inertia':False #该角色是否具有惯性(在使用运动类方法时是否持续移动)。
    }

def update(n):
    roles=n['roles']
    width=n['width']
    height=n['height']
    
    for index in range(len(roles)):
        
        role=roles[index]
        phattr=role.physical_attributes
        #mass=phattr['mass']#该功能已被弃用
        elasticity=phattr['elasticity']
        e=phattr['exercise']
        angle=phattr['gravityAngle']
        byg=phattr['Be affected by gravity']
        pb=phattr['Physical boundary']
        Inertia=phattr['Inertia']
        role.physical_attributes['Inertia']=False
        if byg:
            e[0]+=((1j**(angle/90)).real)*G
            e[1]+=((1j**(angle/90)).imag)*G
        role.xymove(e[0],e[1])
        if 'n' in pb and role.meet_edge('n'):
            role.setY(-height/2+role.attribute('height')/2)
            e[1]*=-elasticity
        if 's' in pb and role.meet_edge('s'):
            role.setY(height/2-role.attribute('height')/2)
            e[1]*=-elasticity
        if 'w' in pb and role.meet_edge('w'):
            role.setX(-width/2+role.attribute('width')/2)
            e[0]*=-elasticity
        if 'e' in pb and role.meet_edge('e'):
            role.setX(width/2-role.attribute('width')/2)
            e[0]*=-elasticity
        phattr['Inertia']=Inertia
