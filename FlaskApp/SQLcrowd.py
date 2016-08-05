import psycopg2
class SQLcrowd(object):
    def __init__(self, dbname):
        self.dbname = dbname

    def conectar(self):
	return psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" % (self.dbname, "postgres", "localhost", "mmae2010"))

    def login(self, user, passwd):
        pass

    def update(self,tabla, variables, condiciones=None):
        conn = self.conectar()
        cur = conn.cursor()
        sql = "UPDATE "+tabla+" SET "
        for variable in variables:
            sql = sql + variable[0] +"='"+variable[1]+"',"
        sql = sql + ","
        sql = sql.replace(",,", "")+" WHERE"
        for condicion in condiciones:
            sql=sql+" "+condicion[0]+"='"+condicion[1]+"'"
        print sql
        cur.execute(sql)
        conn.commit()
        cur.close()
    def delete(self,tabla, condiciones=None):
        conn = self.conectar()
        cur = conn.cursor()
        sql = "DELETE FROM "+tabla+" WHERE"
        for i in range(len(condiciones)):
            sql=sql+" "+condiciones[i][0]+"='"+condiciones[i][1]+"'"
            if i+1!= len(condiciones):
                sql=sql+" and "
        print sql
        cur.execute(sql)
        conn.commit()
        cur.close()


    def Noticias(self, num):
        conn = self.conectar()
        cur = conn.cursor()
        sql = "select id,nombre,rut,responsable,database from usuario_empresas, empresas where usuario_id = " + str(
            user) + " and empresa_id = id order by id"
        cur.execute(sql)


    def Eventos(self, num):
        conn = self.conectar()
        cur = conn.cursor()

    def execute(self,sql,fecthone=False):
        conn = self.conectar()
        cur = conn.cursor()
        cur.execute(sql)
        if fecthone:
            rows = cur.fetchone()
        else:
            rows = cur.fetchall()
        return rows

    def selectpaginador(self, tabla):
        sql = "select last_value from %s_id_seq" % (tabla)
        conn = self.conectar()
        cur = conn.cursor()
        cur.execute(sql)
        last = cur.fetchone()[0]
        divisor=9
        pagina = last / divisor + 1 - pow(0, last % divisor)
        return pagina


    def select(self, tabla, variables, condiciones=None,fecthone=False):
        conn = self.conectar()
        cur = conn.cursor()
        sql = "Select "
        for variable in variables:
            sql = sql + variable + ","
        sql = sql + ","
        sql = sql.replace(",,", "")
        sql = sql + " from " + tabla
        for condicion in condiciones:
            sql=sql+" "+condicion[0]+" "+condicion[1]
        print sql
        cur.execute(sql)
        if fecthone:
            rows = cur.fetchone()
        else:
            rows = cur.fetchall()
        return rows


    def insert(self,tabla,variables,data,returnid=False):
        print "holi"
        conn = self.conectar()
        cur = conn.cursor()
        sql = "Insert into "+tabla+" ("
        for variable in variables:
            sql = sql + variable + ","
        sql = sql + ","

        sql = sql + " values  " + "("
        for dato in data:
            sql = sql + "'" + dato +"',"
        sql = sql + ","
        
        sql = sql.replace(",,", ")")
        if returnid!=False:
            sql=sql+"RETURNING id"
            cur.execute(sql)
            conn.commit()
            return cur.fetchone()[0]
        cur.execute(sql)
        conn.commit()
