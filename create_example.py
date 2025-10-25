"""
Example RBXMX file for testing
This is a simple Model with a script
"""
EXAMPLE_RBXMX = '''<roblox xmlns:xmime="http://www.w3.org/2005/05/xmlmime" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://www.roblox.com/roblox.xsd" version="4">
	<Item class="Model" referent="RBX0">
		<Properties>
			<string name="Name">TestModel</string>
		</Properties>
		<Item class="Part" referent="RBX1">
			<Properties>
				<string name="Name">MainPart</string>
			</Properties>
			<Item class="Script" referent="RBX2">
				<Properties>
					<string name="Name">TestScript</string>
					<ProtectedString name="Source">print("Hello from RBXMX to Rojo!")</ProtectedString>
				</Properties>
			</Item>
		</Item>
		<Item class="Folder" referent="RBX3">
			<Properties>
				<string name="Name">Scripts</string>
			</Properties>
			<Item class="ModuleScript" referent="RBX4">
				<Properties>
					<string name="Name">TestModule</string>
					<ProtectedString name="Source">local module = {}

function module.test()
	print("Module function called")
end

return module</ProtectedString>
				</Properties>
			</Item>
		</Item>
	</Item>
</roblox>'''


if __name__ == "__main__":
    import os
    from pathlib import Path
    
    # Create examples directory
    examples_dir = Path(__file__).parent / "examples"
    examples_dir.mkdir(exist_ok=True)
    
    # Write example file
    example_file = examples_dir / "example.rbxmx"
    example_file.write_text(EXAMPLE_RBXMX, encoding='utf-8')
    
    print(f"Example RBXMX file created at: {example_file}")
