class LCarnitineInterpreter(Exception):
    
    def __init__(self, return_value=None):
        self.return_value = return_value
    
    def env_lookup(self, var_name, env):
        #return env.get(var_name, None) # gets var name at dict key, else returns None (no KeyError)
        if var_name in env[1]: 
            return (env[1])[var_name] 
        elif env[0] == None: # global env
            return None
        else:
            return self.env_lookup(var_name, env[0]) 
    
    def env_update(self, var_name, value, env): # may want to make env class variable
        if var_name in env[1]:
            (env[1])[var_name] = value
        elif not (env[0] == None):
            self.env_update(var_name, value, env[0])
        # print(f'var_name is {var_name}')
        # env[var_name] = value  
    
    def global_env_update(self, var_name, value, env):
        if var_name in env[1] or (env[0] == None):
                (env[1])[var_name] = value
        elif not (env[0] == None):
                self.global_env_update(var_name, value, env[0])
    
    # maybe add env_debug if needed here
    def eval_elt(self, elt, env):
        if elt[0] == 'function':
            fname = elt[1] 
            fparams = elt[2]
            fbody = elt[3]
            fvalue = ("function",fparams,fbody,env) 
            (env[1])[fname] = fvalue
            
        elif elt[0] == 'stmt':
            #print(elt[1])
            self.eval_stmt(elt[1],env) 
        else:
            print(f'ERROR: eval_elt: unknown element {elt}') 

    # added environment to args
    def eval_exp(self, tree, environment):
        node_type = tree[0]

        if node_type == "number":
            return float(tree[1])
        elif node_type == "string": # added these
            return tree[1] 
        elif node_type == "true":
            return True
        elif node_type == "false":
            return False
        elif node_type == "not":
            return not(self.eval_exp(tree[1], environment)) # end added
        elif node_type == "function":
            fparams = tree[1]
            fbody = tree[2]
            return ("function", fparams, fbody, environment)
        elif node_type == "binop":
            left_value = self.eval_exp(tree[1], environment)
            operator = tree[2]
            #print(f'operator is {operator}')
            right_value = self.eval_exp(tree[3], environment)
            if operator =="+":
                return left_value + right_value
            elif operator =="-":
                return left_value - right_value
            elif operator =="/":
                return left_value / right_value
            elif operator =="*":
                return left_value * right_value
            elif operator == "Or it is the case that:":
                return left_value or right_value # this should work for all binops?
            elif operator == "Is equal to the value of:":
                return left_value == right_value
            elif operator == "Is less than or equal to:":
                return left_value <= right_value
            elif operator == "Is less than:":
                return left_value < right_value
            elif operator == "Is greater than or equal to:":
                return left_value >= right_value
            elif operator == "Is greater than:":
                return left_value > right_value
            elif operator == "And it is also the case that:":
                return left_value and right_value
            else:
                print(f'Error: unkown binary operator {operator}')
                exit(1)
            
        elif node_type == "identifier":
            # tree[1] is variable name
            var_name = tree[1]
            value = self.env_lookup(var_name, environment)
            if value == None:
                print(f"Error: No such variable {var_name} exists, ya jabroni.")
            else:
                return value
        
        elif node_type == "call":
            fname = tree[1]
            args = tree[2]
            fvalue = self.env_lookup(fname, environment)
            if fname == "PrintToCLI":
                argval = self.eval_exp(args[0], environment)
                print(str(argval))
                #output_sofar = self.env_lookup("output", environment)
                #self.env_update(environment, "output", output_sofar+str(argval))
            elif fvalue[0] == "function":
                fparams = fvalue[1]
                fbody = fvalue[2]
                fenv = fvalue[3]
                if len(fparams) != len(args):
                    print(f'Error: wrong number of arguments to {fname}')
                else:
                    # make new environment frame
                    newenv = (fenv, {}) # this defines a tuple
                    for i in range(len(args)):
                        argval = self.eval_exp(args[i], environment)
                        (newenv[1])[fparams[i]] = argval
                    # evaluate the body in the new frame
                    try: 
                        self.eval_stmts(fbody, newenv)
                        return None
                    except LCarnitineInterpreter as l:
                        return l.return_value 
            else:
                print(f'Error: call to non-function {fname}')
        else:
            print("Error: unknown expression type.")
        return None

    def eval_stmts(self, stmts,env): 
        for stmt in stmts:
                self.eval_stmt(stmt,env) 

    def eval_stmt(self, stmt, env):
        stype = stmt[0] 
        if stype == "if-then":
            cexp = stmt[1]
            then_branch = stmt[2] 
            if self.eval_exp(cexp,env):
                    self.eval_stmts(then_branch,env) 
        # elif stype == "while":
        #     cexp = stmt[1]
        #     while_body = stmt[2] 
        #     while eval_exp(cexp,env):
        #         eval_stmts(while_body,env) 
        elif stype == "if-then-else":
            cexp = stmt[1]
            then_branch = stmt[2] 
            else_branch = stmt[3] 
            if self.eval_exp(cexp,env):
                self.eval_stmts(then_branch,env) 
            else:
                self.eval_stmts(else_branch,env) 
        elif stype == "var": 
            vname = stmt[1]
            rhs = stmt[2]
            (env[1])[vname] = self.eval_exp(rhs,env)
            # env_update(vname, eval_exp(rhs,env), env) 
        elif stype == "assign": 
            vname = stmt[1]
            rhs = stmt[2] # right hand side?
            self.global_env_update(vname, eval_exp(rhs,env), env)
               
        elif stype == "return": 
            self.retval = self.eval_exp(stmt[1],env) 
            raise LCarnitineInterpreter(self.retval) 
        elif stype == "exp": 
            self.eval_exp(stmt[1],env) 
        else:
            print(f"ERROR: unknown statement type {stype}")
    
    def interpret(self, ast):
        global_env = (None, {"output": ""}) 
        for element in ast:
                #print(element)
                self.eval_elt(element, global_env) 
              #env_debug(global_env)
        #self.eval_stmts(ast, global_env)
        return (global_env[1])["output"]
    
    