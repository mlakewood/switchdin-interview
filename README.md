
# How to run locally

## Dependencies

All that is needed is docker and docker-compose installed and you can run this locally. Please refer to how to install docker on your chosen local environment for more info

## How to run

Change into the root repo and run

```docker compose up```

This should pull down the required containers and start them, and output the report of the data coming through.

## What else could be done

1. Testing

There currently arent any tests. This is not a thing I would ever do in a real system, however in this one it was a little tricky as the system actually kinda tests itself. I bias for end to end tests where ever I can. One way to make this system work in that way would be to store the result in the reporting service somewhere and then query it over time. But this was out of scope for the excercise.


2. Observability

With any system like this, having observability data is paramount. Tracing would be idea in this situation to tell where everything is going.

3. The paho client. 

I purposly used the paho client as simply as I could in this instance, really only using the publish and subscribe modules. This cuts off some interesting ways of testing, as you never get your hands on the actual client. Normally I would inject a client into the function that is using it as a parameter, so that in test, you could modify this in a way to get more flexible test environment.

4. Ansible

I do have some of the spin up of the ec2 instance automated through Ansible, but I think there is an impedance mismatch here between spinning up infra and configuring it. I think Ansible is good at the latter and kinda clunky at the former. I will say this is the first time I have used Ansible, so take that with a grain of salt.

5. MQTT Semantics

As I was reading the paho docs I noticed that there was a lot of tuning that could be done to the client (and likely the broker). In a real application taking notice of these settings is imperative as well as the semantics of the storage tech/queue mechanism. However in this instance I have ignored almost all of them.

