=======
Methods
=======

Low-level API method objects. Each class corresponds to one Rubika
Bot API endpoint and is callable via ``await bot(method_instance)``.

.. autoclass:: aiorubi.methods.base.RubikaMethod
   :members:

.. autoclass:: aiorubi.methods.base.Request
   :members:

.. autoclass:: aiorubi.methods.base.Response
   :members:

Chat members
============

.. autoclass:: aiorubi.methods.ban_chat_member.BanChatMember
   :members:
   :special-members: __init__

.. autoclass:: aiorubi.methods.unban_chat_member.UnbanChatMember
   :members:
   :special-members: __init__

Files
=====

.. autoclass:: aiorubi.methods.get_file.GetFile
   :members:
   :special-members: __init__

.. autoclass:: aiorubi.methods.request_send_file.RequestSendFile
   :members:
   :special-members: __init__

.. autoclass:: aiorubi.methods.send_file.SendFile
   :members:
   :special-members: __init__

.. autoclass:: aiorubi.methods.upload_file.UploadFile
   :members:
   :special-members: __init__

Messaging
=========

.. autoclass:: aiorubi.methods.send_message.SendMessage
   :members:
   :special-members: __init__

.. autoclass:: aiorubi.methods.send_contact.SendContact
   :members:
   :special-members: __init__

.. autoclass:: aiorubi.methods.send_location.SendLocation
   :members:
   :special-members: __init__

.. autoclass:: aiorubi.methods.send_poll.SendPoll
   :members:
   :special-members: __init__

.. autoclass:: aiorubi.methods.edit_message_text.EditMessageText
   :members:
   :special-members: __init__

.. autoclass:: aiorubi.methods.delete_message.DeleteMessage
   :members:
   :special-members: __init__

.. autoclass:: aiorubi.methods.forward_message.ForwardMessage
   :members:
   :special-members: __init__

Keypads
=======

.. autoclass:: aiorubi.methods.edit_chat_keypad.EditChatKeypad
   :members:
   :special-members: __init__

.. autoclass:: aiorubi.methods.edit_message_keypad.EditMessageKeypad
   :members:
   :special-members: __init__

Updates
=======

.. autoclass:: aiorubi.methods.get_updates.GetUpdates
   :members:
   :special-members: __init__

.. autoclass:: aiorubi.methods.get_me.GetMe
   :members:
   :special-members: __init__

.. autoclass:: aiorubi.methods.get_chat.GetChat
   :members:
   :special-members: __init__

.. autoclass:: aiorubi.methods.set_commands.SetCommands
   :members:
   :special-members: __init__

.. autoclass:: aiorubi.methods.update_bot_endpoints.UpdateBotEndpoints
   :members:
   :special-members: __init__
