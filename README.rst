ansible-inline-vault
====================

Setup:

- create ``.vault_pass`` or an executable ``.vault_pass.py``:

  .. code-block:: console

    $ cat >.vault_pass <<EOF
    #!/bin/sh
    echo -n secret_password
    EOF

  .. code-block:: console

    $ chmod 755 .vault_pass

- create your data file:

  .. code-block:: console

    $ cat >some_file.ini <<EOF
    username = john
    password = secret_password
    EOF

- make passwords secret, by running ``ansible-inline-vault encrypt-string``:

  .. code-block:: console

    $ ansible-vault encrypt-string
    Reading plaintext input from stdin
    secret_password^D^D
    {{ "$ANSIBLE_VAULT;1.1;AES256\n3238...3266"|decrypt }}

- replace password in data file and save as ``some_file.ini.j2``:

  .. code-block:: dosini

    username = john
    password = {{ "$ANSIBLE_VAULT;1.1;AES256\n3238...3266"|decrypt }}

- decrypt using ``ansible-inline-vault decrypt``:

  .. code-block:: console

    $ ansible-inline-vault decrypt some_file.ini.j2
    username = john
    password = secret_password


Example Makefile
----------------

::

    VAULT_BIN = /usr/local/bin/ansible-inline-vault

    values.yaml: $(VAULT_BIN) values.yaml.j2
    	$(VAULT_BIN) decrypt values.yaml.j2 >$@

    $(VAULT_BIN):
    	@echo "ansible-inline-vault not found. Please do:" >&2
    	@echo >&2
    	@echo "  sudo -H pip3 install git+https://github.com/ossobv/ansible-inline-vault#main" >&2
    	@echo >&2
    	@false

Please ``values.yaml`` in ``.gitignore`` while you can commit
``.vault_pass`` as long as it does not contain the secret itself.
