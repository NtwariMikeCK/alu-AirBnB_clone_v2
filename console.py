#!/usr/bin/python3
""" Console Module """
import cmd
import sys
from models.base_model import BaseModel
from models.__init__ import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """ Contains the functionality for the HBNB console"""

    # determines prompt for interactive/non-interactive modes
    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''

    classes = {
               'BaseModel': BaseModel, 'User': User, 'Place': Place,
               'State': State, 'City': City, 'Amenity': Amenity,
               'Review': Review
              }
    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']
    types = {
             'number_rooms': int, 'number_bathrooms': int,
             'max_guest': int, 'price_by_night': int,
             'latitude': float, 'longitude': float
            }

    def preloop(self):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb)')

    def precmd(self, line):
        """Reformat command line for advanced command syntax.

        Usage: <class name>.<command>([<id> [<*args> or <**kwargs>]])
        (Brackets denote optional fields in usage example.)
        """
        _cmd = _cls = _id = _args = ''  # initialize line elements

        # scan for general formating - i.e '.', '(', ')'
        if not ('.' in line and '(' in line and ')' in line):
            return line

        try:  # parse line left to right
            pline = line[:]  # parsed line

            # isolate <class name>
            _cls = pline[:pline.find('.')]

            # isolate and validate <command>
            _cmd = pline[pline.find('.') + 1:pline.find('(')]
            if _cmd not in HBNBCommand.dot_cmds:
                raise Exception

            # if parantheses contain arguments, parse them
            pline = pline[pline.find('(') + 1:pline.find(')')]
            if pline:
                # partition args: (<id>, [<delim>], [<*args>])
                pline = pline.partition(', ')  # pline convert to tuple

                # isolate _id, stripping quotes
                _id = pline[0].replace('\"', '')
                # possible bug here:
                # empty quotes register as empty _id when replaced

                # if arguments exist beyond _id
                pline = pline[2].strip()  # pline is now str
                if pline:
                    # check for *args or **kwargs
                    if pline[0] == '{' and pline[-1] == '}' 
                    and type(eval(pline)) is dict:
                        _args = pline
                    else:
                        _args = pline.replace(',', '')
                        # _args = _args.replace('\"', '')
            line = ' '.join([_cmd, _cls, _id, _args])

        except Exception as mess:
            pass
        finally:
            return line

    def postcmd(self, stop, line):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb) ', end='')
        return stop

    def do_quit(self, command):
        """ Method to exit the HBNB console"""
        exit()

    def help_quit(self):
        """ Prints the help documentation for quit  """
        print("Exits the program with formatting\n")

    def do_EOF(self, arg):
        """ Handles EOF to exit program """
        print()
        exit()

    def help_EOF(self):
        """ Prints the help documentation for EOF """
        print("Exits the program without formatting\n")

    def emptyline(self):
        """ Overrides the emptyline method of CMD """
        pass

    
    def do_create(self, args):
        """This modifies our create method"""
        # Check for the args provided
        if not args:
            print("** class name missing **")
            return

        args = args.split(" ", 1)  # Split by the first space
        c_name = args[0]

        if c_name not in HBNBCommand.classes:  # Class name invalid
            print("** class doesn't exist **")
            return
        # Create an instance of the class
        new_instance = HBNBCommand.classes[c_name]()
        item_dict = {}
        # new_instance.save()
        

        # Process the parameters
        # if len(args) > 1:
        #     params = args[1].replace("(", "").replace(")", "").split()  # Handle parentheses and split
        if len(args) > 1:
            param_string = args[1]
            param_list = param_string.split()  # Split parameters by space
            i = 0
            while i < len(param_list):
                param = param_list[i]
                if "=" in param:  # Handle key=value format
                    key, value = param.split("=", 1)
                else:  # Handle key value format
                    if i + 1 < len(param_list):
                        key = param
                        value = param_list[i + 1]
                        i += 1  # Skip the next item as it is the value
                    else:
                        print(f"Ignored invalid parameter: {param}")
                        break

                # Process value
                if value.startswith('"') and value.endswith('"'):  # Quoted strings
                    value = value[1:-1].replace("_", " ")
                elif value.isdigit():  # Integer values
                    value = int(value)
                elif value.replace('.', '', 1).isdigit():  # Float values
                    value = float(value)
                else:
                    value = value  # Keep as string

                # Add to the dictionary
                item_dict[key] = value
                i += 1

        update_args = f"{c_name} {new_instance.id} "  # Start with class name and instance ID
        for key, value in item_dict.items():
            update_args += f"{key} {value} "  # Add each key-value pair

        # Call `do_update` with the formatted string
        print(new_instance.id)
        self.do_update(update_args.strip())



    def help_create(self):
        """ Help information for the create method """
        print("Creates a class of any type")
        print("[Usage]: create <className>\n")

    def do_show(self, args):
        """ Method to show an individual object """
        new = args.partition(" ")
        c_name = new[0]
        c_id = new[2]

        # guard against trailing args
        if c_id and ' ' in c_id:
            c_id = c_id.partition(' ')[0]

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id
        try:
            print(storage._FileStorage__objects[key])
        except KeyError:
            print("** no instance found **")

    def help_show(self):
        """ Help information for the show command """
        print("Shows an individual instance of a class")
        print("[Usage]: show <className> <objectId>\n")

    def do_destroy(self, args):
        """ Destroys a specified object """
        new = args.partition(" ")
        c_name = new[0]
        c_id = new[2]
        if c_id and ' ' in c_id:
            c_id = c_id.partition(' ')[0]

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id

        try:
            del(storage.all()[key])
            storage.save()
        except KeyError:
            print("** no instance found **")

    def help_destroy(self):
        """ Help information for the destroy command """
        print("Destroys an individual instance of a class")
        print("[Usage]: destroy <className> <objectId>\n")

    def do_all(self, args):
        """ Shows all objects, or all objects of a class"""
        print_list = []

        if args:
            args = args.split(' ')[0]  # remove possible trailing args
            if args not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return
            for k, v in storage._FileStorage__objects.items():
                if k.split('.')[0] == args:
                    print_list.append(str(v))
        else:
            for k, v in storage._FileStorage__objects.items():
                print_list.append(str(v))

        print(print_list)

    def help_all(self):
        """ Help information for the all command """
        print("Shows all objects, or all of a class")
        print("[Usage]: all <className>\n")

    def do_count(self, args):
        """Count current number of class instances"""
        count = 0
        for k, v in storage._FileStorage__objects.items():
            if args == k.split('.')[0]:
                count += 1
        print(count)

    def help_count(self):
        """ """
        print("Usage: count <class_name>")

    def do_update(self, args):
        """Updates a certain object with new info."""
        c_name = c_id = att_name = att_val = kwargs = ''

        # Split the class name and the rest of the arguments
        args = args.partition(" ")
        if args[0]:
            c_name = args[0]
        else:  # Class name not provided
            print("** class name missing **")
            return
        if c_name not in HBNBCommand.classes:  # Invalid class name
            print("** class doesn't exist **")
            return

        # Split the instance ID and the rest of the arguments
        args = args[2].partition(" ")
        if args[0]:
            c_id = args[0]
        else:  # Instance ID not provided
            print("** instance id missing **")
            return

        # Generate the key to check for the object
        key = c_name + "." + c_id

        # Check if the object exists
        if key not in storage.all():
            print("** no instance found **")
            return

        # Retrieve the object
        obj = storage.all()[key]

        # Check if attributes are passed as a dictionary
        if '{' in args[2] and '}' in args[2] and type(eval(args[2])) is dict:
            kwargs = eval(args[2])  # Parse the dictionary
            for k, v in kwargs.items():
                if hasattr(obj, k):
                    # Cast to the correct type if specified in `HBNBCommand.types`
                    if k in HBNBCommand.types:
                        v = HBNBCommand.types[k](v)
                    setattr(obj, k, v)  # Set the attribute
        else:
            # Process remaining arguments as key-value pairs
            params = args[2].split()  # Split the remaining arguments
            if len(params) % 2 != 0:  # Ensure there is an even number of arguments
                print("** attribute name or value missing **")
                return

            # Iterate through pairs of key-value arguments
            for i in range(0, len(params), 2):
                att_name = params[i]
                att_val = params[i + 1]

                # Cast to the correct type if specified in `HBNBCommand.types`
                if att_name in HBNBCommand.types:
                    att_val = HBNBCommand.types[att_name](att_val)
                setattr(obj, att_name, att_val)  # Set the attribute
        obj.save()  # Save updates to storage

    def help_update(self):
        """ Help information for the update class """
        print("Updates an object with new information")
        print("Usage: update <className> <id> <attName> <attVal>\n")


if __name__ == "__main__":
    HBNBCommand().cmdloop()
